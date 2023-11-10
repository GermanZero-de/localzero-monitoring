from collections import Counter
from datetime import date
import json
import os
import time
import uuid

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from invitations import views as invitations_views
from invitations.app_settings import app_settings as invitations_settings
from invitations.adapters import get_invitations_adapter
from invitations.views import accept_invitation
from martor.utils import LazyEncoder
from PIL import Image

from .models import (
    AccessRight,
    City,
    ExecutionStatus,
    Task,
    CapChecklist,
    AdministrationChecklist,
)

STATUS_ORDER = [
    ExecutionStatus.FAILED,
    ExecutionStatus.DELAYED,
    ExecutionStatus.AS_PLANNED,
    ExecutionStatus.COMPLETE,
    ExecutionStatus.UNKNOWN,
]

TO_STATUS = {status.value: status for status in ExecutionStatus}


def _show_drafts(request):
    return request.user.is_authenticated


def _calculate_summary(request, node):
    """calculate summarized status for a given node or a whole city"""

    if isinstance(node, City):
        subtasks = Task.objects.filter(city=node, numchild=0)
    else:
        subtasks = node.get_descendants().filter(numchild=0)
    if not _show_drafts(request):
        subtasks = subtasks.filter(draft_mode=False)

    subtasks_count = len(subtasks)
    status_counts = Counter(
        [TO_STATUS[subtask.execution_status] for subtask in subtasks]
    )
    status_proportions = {
        status: round(count / subtasks_count * 100)
        for status, count in status_counts.items()
    }

    node.status_proportions = _sort_status_proportions(status_proportions, STATUS_ORDER)
    node.subtasks_count = subtasks_count
    node.complete_proportion = status_proportions.get(ExecutionStatus.COMPLETE, 0)
    node.incomplete_proportion = 100 - node.complete_proportion


def _sort_status_proportions(
    status_proportions: dict[ExecutionStatus, int], order: list[ExecutionStatus]
) -> list[tuple[int, ExecutionStatus]]:
    status_proportions_sorted = []
    for status in order:
        if status in status_proportions.keys():
            status_proportions_sorted.append((status_proportions[status], status))
    return status_proportions_sorted


def _get_frontpage_tasks(request, city):
    tasks = Task.objects.filter(city=city, numchild=0, frontpage=1)
    if not _show_drafts(request):
        if city.draft_mode:
            tasks = tasks.none()
        else:
            tasks = tasks.filter(draft_mode=False)

    return tasks


def _get_children(request, city, node=None):
    if not node:
        children = Task.get_root_nodes().filter(city=city)
    else:
        children = node.get_children()
    if not _show_drafts(request):
        if city.draft_mode:
            children = children.none()
        else:
            children = children.filter(draft_mode=False)

    groups = children.filter(numchild__gt=0)
    tasks = children.filter(numchild=0)
    for group in groups:
        _calculate_summary(request, group)

    return groups, tasks


def _get_cities(request, slug=None):
    try:
        cities = City.objects.all()
        if not _show_drafts(request):
            cities = cities.filter(draft_mode=False)
        if slug:
            return cities.get(slug=slug)
        else:
            return cities.order_by("name")
    except City.DoesNotExist:
        return None


def _get_base_context(request):
    return {
        "cities": _get_cities(request),
    }


def _get_breadcrumbs(*args):
    breadcrumbs = [{"label": "Start", "url": reverse("index")}]
    breadcrumbs += args
    return breadcrumbs


# Our main page
def index_view(request):
    return render(request, "index.html", _get_base_context(request))


def city_view(request, city_slug):
    city = _get_cities(request, city_slug)
    if not city:
        raise Http404(f"Wir haben keine Daten zu der Kommune '{city_slug}'.")

    _calculate_summary(request, city)

    cap_checklist = _get_cap_checklist(city)
    cap_checklist_exists = cap_checklist != {}

    administration_checklist = _get_administration_checklist(city)
    administration_checklist_exists = administration_checklist != {}

    breadcrumbs = _get_breadcrumbs(
        {"label": city.name, "url": reverse("city", args=[city_slug])},
    )

    context = _get_base_context(request)
    context.update(
        {
            "breadcrumbs": breadcrumbs,
            "city": city,
            "charts": city.charts.all,
            "cap_checklist_exists": cap_checklist_exists,
            "administration_checklist_exists": administration_checklist_exists,
            "asmt_admin": city.assessment_administration,
            "asmt_plan": city.assessment_action_plan,
            "asmt_status": city.assessment_status,
            "local_group": getattr(city, "local_group", None),
            "tasks": _get_frontpage_tasks(request, city),
        }
    )

    if cap_checklist_exists:
        cap_checklist_total = len(cap_checklist)
        cap_checklist_number_fulfilled = _count_checklist_number_fulfilled(
            cap_checklist
        )
        cap_checklist_proportion_fulfilled = round(
            cap_checklist_number_fulfilled / cap_checklist_total * 100
        )

        context.update(
            {
                "cap_checklist_total": cap_checklist_total,
                "cap_checklist_number_fulfilled": cap_checklist_number_fulfilled,
                "cap_checklist_proportion_fulfilled": cap_checklist_proportion_fulfilled,
            }
        )

    if administration_checklist_exists:
        administration_checklist_total = len(administration_checklist)
        administration_checklist_number_fulfilled = _count_checklist_number_fulfilled(
            administration_checklist
        )
        administration_checklist_proportion_fulfilled = round(
            administration_checklist_number_fulfilled
            / administration_checklist_total
            * 100
        )
        context.update(
            {
                "administration_checklist_total": administration_checklist_total,
                "administration_checklist_number_fulfilled": administration_checklist_number_fulfilled,
                "administration_checklist_proportion_fulfilled": administration_checklist_proportion_fulfilled,
            }
        )

    if city.resolution_date and city.target_year:
        target_date = date(city.target_year, 12, 31)
        days_total = (target_date - city.resolution_date).days + 1
        days_gone = (date.today() - city.resolution_date).days
        days_left = days_total - days_gone
        years_left = round(days_left / 365)
        days_remain = days_left % 365
        days_gone_proportion = round(days_gone / days_total * 100)
        days_left_proportion = round(days_left / days_total * 100)
        context.update(
            {
                "days_gone": days_gone,
                "days_left": days_left,
                "years_left": years_left,
                "days_remain": days_remain,
                "days_gone_proportion": days_gone_proportion,
                "days_left_proportion": days_left_proportion,
            }
        )

    return render(request, "city.html", context)


def cap_checklist_view(request, city_slug):
    city = _get_cities(request, city_slug)
    if not city:
        raise Http404(f"Wir haben keine Daten zu der Kommune '{city_slug}'.")

    breadcrumbs = _get_breadcrumbs(
        {"label": city.name, "url": reverse("city", args=[city_slug])},
        {"label": "KAP Checkliste", "url": reverse("cap_checklist", args=[city_slug])},
    )

    context = _get_base_context(request)
    context.update(
        {
            "breadcrumbs": breadcrumbs,
            "city": city,
            "cap_checklist": _get_cap_checklist(city),
        }
    )
    return render(request, "cap_checklist.html", context)


def _get_cap_checklist(city) -> dict:
    try:
        checklist = city.cap_checklist
    except CapChecklist.DoesNotExist:
        return {}

    return _as_formatted_checklist(checklist)


def _as_formatted_checklist(checklist):
    checkbox_items = [
        field
        for field in checklist._meta.get_fields()
        if field.attname not in ["city_id", "id"] and "_rationale" not in field.attname
    ]

    return {
        checkbox_item.verbose_name: {
            "is_checked": getattr(checklist, checkbox_item.attname),
            "help_text": checkbox_item.help_text,
            "rationale": getattr(checklist, checkbox_item.attname + "_rationale"),
        }
        for checkbox_item in checkbox_items
    }


def administration_checklist_view(request, city_slug):
    city = _get_cities(request, city_slug)
    if not city:
        raise Http404(f"Wir haben keine Daten zu der Kommune '{city_slug}'.")

    breadcrumbs = _get_breadcrumbs(
        {"label": city.name, "url": reverse("city", args=[city_slug])},
        {
            "label": "Verwaltung Checkliste",
            "url": reverse("administration_checklist", args=[city_slug]),
        },
    )

    context = _get_base_context(request)
    context.update(
        {
            "breadcrumbs": breadcrumbs,
            "city": city,
            "administration_checklist": _get_administration_checklist(city),
        }
    )

    return render(request, "administration_checklist.html", context)


def _get_administration_checklist(city) -> dict:
    try:
        checklist = city.administration_checklist
    except AdministrationChecklist.DoesNotExist:
        return {}

    return _as_formatted_checklist(checklist)


def _count_checklist_number_fulfilled(checklist_items: dict):
    count = 0

    for _, values in checklist_items.items():
        for _, is_checked in values.items():
            if is_checked is True:
                count += 1

    return count


def _get_task(request, city, task_slugs):
    task = Task.objects.get(city=city, slugs=task_slugs)
    if task.draft_mode and not _show_drafts(request):
        raise Task.DoesNotExist()
    return task


def task_view(request, city_slug, task_slugs=None):
    context = _get_base_context(request)

    city = _get_cities(request, city_slug)
    if not city:
        raise Http404(f"Wir haben keine Daten zu der Kommune '{city_slug}'.")

    breadcrumbs = _get_breadcrumbs(
        {"label": city.name, "url": reverse("city", args=[city_slug])},
        {"label": "Maßnahmen", "url": reverse("task", args=[city_slug])},
    )

    if not task_slugs:
        groups, tasks = _get_children(request, city)

        context.update(
            {"breadcrumbs": breadcrumbs, "city": city, "groups": groups, "tasks": tasks}
        )

        return render(
            request,
            "taskgroup.html",
            context,
        )

    try:
        task: Task = _get_task(request, city, task_slugs)
    except Task.DoesNotExist:
        raise Http404(
            "Wir haben keine Daten zu dem Handlungsfeld / der Maßnahme '%s'."
            % task_slugs
        )

    breadcrumbs += [
        {
            "label": ancestor.title,
            "url": reverse("task", args=[city_slug, ancestor.slugs]),
        }
        for ancestor in task.get_ancestors()
    ] + [{"label": task.title, "url": reverse("task", args=[city_slug, task.slugs])}]

    context.update({"breadcrumbs": breadcrumbs, "city": city, "node": task})

    if task.is_leaf():
        return render(
            request,
            "task.html",
            context,
        )
    else:
        groups, tasks = _get_children(request, city, task)

        context.update({"groups": groups, "tasks": tasks})
        return render(
            request,
            "taskgroup.html",
            context,
        )


def project_view(request):
    breadcrumbs = _get_breadcrumbs(
        {"label": "Projekt", "url": reverse("project")},
    )
    context = _get_base_context(request)
    context.update({"breadcrumbs": breadcrumbs})
    return render(request, "project.html", context)


def impressum_view(request):
    return render(request, "impressum.html", _get_base_context(request))


def datenschutz_view(request):
    return render(request, "datenschutz.html", _get_base_context(request))


def ueber_uns_view(request):
    breadcrumbs = _get_breadcrumbs(
        {"label": "Über uns", "url": reverse("ueber-uns")},
    )
    context = _get_base_context(request)
    context.update({"breadcrumbs": breadcrumbs})
    return render(request, "ueber-uns.html", context)


def local_group_view(request, city_slug):
    city = _get_cities(request, city_slug)
    breadcrumbs = _get_breadcrumbs(
        {"label": city.name, "url": reverse("city", args=[city_slug])},
        {"label": "Lokalgruppe", "url": reverse("local_group", args=[city_slug])},
    )

    context = _get_base_context(request)
    context.update(
        {"breadcrumbs": breadcrumbs, "city": city, "local_group": city.local_group}
    )
    return render(request, "local-group.html", context)


@login_required
def markdown_uploader_view(request):
    if request.method != "POST":
        return HttpResponse(_("Invalid request!"))
    if "markdown-image-upload" not in request.FILES:
        return HttpResponse(_("Invalid request!"))

    image = request.FILES["markdown-image-upload"]
    image_types = ["image/png", "image/jpg", "image/jpeg", "image/pjpeg", "image/gif"]
    if image.content_type not in image_types:
        data = json.dumps(
            {
                "status": 415,
                "error": _(
                    "Unsupported image format. Supported formats: "
                    + ", ".join(image_types)
                ),
            },
            cls=LazyEncoder,
        )
        return HttpResponse(data, content_type="application/json", status=415)

    if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
        to_mb = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
        data = json.dumps(
            {
                "status": 413,
                "error": _("Maximum image file is %(size)s MB.") % {"size": to_mb},
            },
            cls=LazyEncoder,
        )
        return HttpResponse(data, content_type="application/json", status=413)

    img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(" ", "-"))
    tmp_file = os.path.join(
        settings.MARTOR_UPLOAD_PATH, time.strftime("%Y/%m/%d/"), img_uuid
    )
    def_path = default_storage.save(tmp_file, ContentFile(image.read()))

    # restrict size to max 2000 width or height
    img_path = os.path.join(settings.MEDIA_ROOT, def_path)
    img = Image.open(img_path)
    if img.width > 2000 or img.height > 2000:
        img.thumbnail((2000, 2000))
        img.save(img_path)

    img_url = os.path.join(settings.MEDIA_URL, def_path)

    data = json.dumps({"status": 200, "link": img_url, "name": image.name})
    return HttpResponse(data, content_type="application/json")


class AcceptInvite(invitations_views.AcceptInvite):
    "Overwrite handling of invitation link."

    def post(self, *args, **kwargs):
        """
        Unfortunately, the whole method had to be copied.
        Identical to base implementation, except where noted.
        """
        self.object = invitation = self.get_object()

        if invitations_settings.GONE_ON_ACCEPT_ERROR and (
            not invitation
            or (invitation and (invitation.accepted or invitation.key_expired()))
        ):
            return HttpResponse(status=410)

        if not invitation:
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                "invitations/messages/invite_invalid.txt",
            )
            return redirect(invitations_settings.LOGIN_REDIRECT)

        if invitation.accepted:
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                "invitations/messages/invite_already_accepted.txt",
                {"email": invitation.email},
            )
            return redirect(invitations_settings.LOGIN_REDIRECT)

        if invitation.key_expired():
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                "invitations/messages/invite_expired.txt",
                {"email": invitation.email},
            )
            return redirect(self.get_signup_redirect())

        if not invitations_settings.ACCEPT_INVITE_AFTER_SIGNUP:
            accept_invitation(
                invitation=invitation,
                request=self.request,
                signal_sender=self.__class__,
            )
            # Difference: Revert accepted to allow reuse of link.
            invitation.accepted = False
            invitation.save()

        user: auth.models.User = self.request.user
        if user.is_authenticated:
            if user.is_active and user.is_staff:
                get_invitations_adapter().add_message(
                    self.request,
                    messages.SUCCESS,
                    "invitations/messages/invite_for_logged_in_user.txt",
                    {
                        "role": invitation.get_access_right_display(),
                        "city": invitation.city.name,
                        "username": user.username,
                    },
                )
                city: City = invitation.city
                if invitation.access_right == AccessRight.CITY_EDITOR:
                    city.city_editors.add(user.pk)
                elif invitation.access_right == AccessRight.CITY_ADMIN:
                    city.city_admins.add(user.pk)
                return redirect(invitations_settings.LOGIN_REDIRECT)
            else:
                get_invitations_adapter().add_message(
                    self.request,
                    messages.ERROR,
                    "invitations/messages/invite_for_logged_in_user_invalid.txt",
                    {"role": str(invitation), "username": user.username},
                )
                auth.logout(self.request)

        # Difference: Saving key and not email.
        self.request.session["invitation_key"] = invitation.key

        return redirect(self.get_signup_redirect())
