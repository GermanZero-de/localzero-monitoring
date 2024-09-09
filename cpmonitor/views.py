import json
import os
import re
import requests
import time
import uuid
from collections import Counter
from datetime import date, datetime

from PIL import Image
from django.conf import settings
from django.contrib import admin
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import Http404, HttpResponseServerError, JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from invitations import views as invitations_views
from invitations.adapters import get_invitations_adapter
from invitations.app_settings import app_settings as invitations_settings
from invitations.views import accept_invitation
from martor.utils import LazyEncoder
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    AccessRight,
    City,
    ExecutionStatus,
    Task,
    CapChecklist,
    AdministrationChecklist,
    EnergyPlanChecklist,
)

from .serializers import CitySerializer
from .serializers import TaskSerializer
from .serializers import TaskWithoutDraftModeSerializer

from .utils import RemainingTimeInfo

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
        sugg_subtasks = Task.objects.filter(
            city=node, numchild=0, source=Task.TaskSource.SUGGESTED
        )
    else:
        subtasks = node.get_descendants().filter(numchild=0)
        sugg_subtasks = node.get_descendants().filter(
            numchild=0, source=Task.TaskSource.SUGGESTED
        )
    if not _show_drafts(request):
        subtasks = subtasks.filter(draft_mode=False)

    subtasks_count = len(subtasks)
    sugg_subtasks_count = len(sugg_subtasks)
    status_counts = Counter(
        [TO_STATUS[subtask.execution_status] for subtask in subtasks]
    )
    sugg_status_counts = Counter(
        [TO_STATUS[sugg_subtask.execution_status] for sugg_subtask in sugg_subtasks]
    )
    status_proportions = {
        status: round(count / subtasks_count * 100)
        for status, count in status_counts.items()
    }
    sugg_status_proportions = {
        status: round(count / sugg_subtasks_count * 100)
        for status, count in sugg_status_counts.items()
    }

    node.status_proportions = _sort_status_proportions(status_proportions, STATUS_ORDER)
    node.sugg_status_proportions = _sort_status_proportions(
        sugg_status_proportions, STATUS_ORDER
    )
    node.subtasks_count = subtasks_count
    node.sugg_subtasks_count = sugg_subtasks_count
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


def _get_task_groups(city):
    children = Task.get_root_nodes().filter(city=city)
    groups = children.filter(depth=1)
    return groups


# def _get_cap_checklist(city) -> CapChecklist | None:
#     cap_checklists = CapChecklist.objects.all().filter(city=city)
#     if len(cap_checklists) > 0:
#         return cap_checklists[0]
#     return None


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

    cap_checklist = _get_cap_checklist_items(city)
    cap_checklist_exists = len(cap_checklist) > 0

    administration_checklist = _get_administration_checklist_items(city)
    administration_checklist_exists = len(administration_checklist) > 0

    energy_plan_checklist = _get_energy_plan_checklist_items(city)
    energy_plan_checklist_exists = len(energy_plan_checklist) > 0

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
            "energy_plan_checklist_exists": energy_plan_checklist_exists,
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

    if energy_plan_checklist_exists:
        energy_plan_checklist_total = len(energy_plan_checklist)
        energy_plan_checklist_number_fulfilled = _count_checklist_number_fulfilled(
            energy_plan_checklist
        )
        energy_plan_checklist_proportion_fulfilled = round(
            energy_plan_checklist_number_fulfilled / energy_plan_checklist_total * 100
        )
        context.update(
            {
                "energy_plan_checklist_total": energy_plan_checklist_total,
                "energy_plan_checklist_number_fulfilled": energy_plan_checklist_number_fulfilled,
                "energy_plan_checklist_proportion_fulfilled": energy_plan_checklist_proportion_fulfilled,
            }
        )

    if city.resolution_date and city.target_year:
        time_info = RemainingTimeInfo(city.resolution_date, city.target_year)
        context.update(
            {
                "days_gone": time_info.days_gone,
                "days_left": time_info.days_left,
                "years_left": time_info.years_left,
                "days_in_year_left": time_info.days_in_year_left,
                "days_gone_proportion": time_info.days_gone_proportion,
                "days_left_proportion": time_info.days_left_proportion,
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
            "cap_checklist": _get_cap_checklist_items(city),
            "local_group": getattr(city, "local_group", None),
        }
    )
    return render(request, "cap_checklist.html", context)


def _get_cap_checklist(city) -> CapChecklist | None:
    try:
        return city.cap_checklist
    except CapChecklist.DoesNotExist:
        return None


def _get_cap_checklist_items(city) -> list:
    checklist = _get_cap_checklist(city)
    if checklist is None:
        return []

    return _as_formatted_checklist(checklist)


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
            "administration_checklist": _get_administration_checklist_items(city),
            "local_group": getattr(city, "local_group", None),
        }
    )

    return render(request, "administration_checklist.html", context)


def _get_administration_checklist(city) -> AdministrationChecklist | None:
    try:
        return city.administration_checklist
    except AdministrationChecklist.DoesNotExist:
        return None


def _get_administration_checklist_items(city) -> list:
    checklist = _get_administration_checklist(city)
    if checklist is None:
        return []

    return _as_formatted_checklist(checklist)


def energy_plan_checklist_view(request, city_slug):
    city = _get_cities(request, city_slug)
    if not city:
        raise Http404(f"Wir haben keine Daten zu der Kommune '{city_slug}'.")

    breadcrumbs = _get_breadcrumbs(
        {"label": city.name, "url": reverse("city", args=[city_slug])},
        {
            "label": "Wärmeplanung Checkliste",
            "url": reverse("energy_plan_checklist", args=[city_slug]),
        },
    )

    context = _get_base_context(request)
    context.update(
        {
            "breadcrumbs": breadcrumbs,
            "city": city,
            "energy_plan_checklist": _get_energy_plan_checklist_items(city),
            "local_group": getattr(city, "local_group", None),
        }
    )

    return render(request, "energy_plan_checklist.html", context)


def _get_energy_plan_checklist(city) -> EnergyPlanChecklist | None:
    try:
        return city.energy_plan_checklist
    except EnergyPlanChecklist.DoesNotExist:
        return None


def _get_energy_plan_checklist_items(city) -> list:
    checklist = _get_energy_plan_checklist(city)
    if checklist is None:
        return []

    return _as_formatted_checklist(checklist)


def _as_formatted_checklist(checklist) -> list:
    checkbox_items = [
        field
        for field in checklist._meta.get_fields()
        if field.attname not in ["city_id", "id"] and "_rationale" not in field.attname
    ]

    return [
        {
            "id": idx,
            "question": checkbox_item.verbose_name,
            "is_checked": getattr(checklist, checkbox_item.attname),
            "help_text": checkbox_item.help_text,
            "rationale": getattr(checklist, checkbox_item.attname + "_rationale"),
        }
        for idx, checkbox_item in enumerate(checkbox_items)
    ]


def _count_checklist_number_fulfilled(checklist_items: list):
    count = 0

    for item in checklist_items:
        if item["is_checked"] is True:
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
            {
                "breadcrumbs": breadcrumbs,
                "city": city,
                "groups": groups,
                "tasks": tasks,
                "local_group": getattr(city, "local_group", None),
            }
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

    context.update(
        {
            "breadcrumbs": breadcrumbs,
            "city": city,
            "local_group": getattr(city, "local_group", None),
        }
    )

    if task.is_leaf():
        context.update({"task": task})
        return render(
            request,
            "task.html",
            context,
        )
    else:
        groups, tasks = _get_children(request, city, task)

        context.update({"node": task, "groups": groups, "tasks": tasks})
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


def mstr_view(request, municipality_key):
    url = "https://www.marktstammdatenregister.de/MaStR/Einheit/EinheitJson/GetVerkleinerteOeffentlicheEinheitStromerzeugung"
    params = {
        "sort": "EinheitMeldeDatum-desc",
        "page": 1,
        "pageSize": 10000,
        "filter": f"Energieträger~eq~'2495'~and~Gemeindeschlüssel~eq~'{municipality_key}'",
    }
    try:
        r = requests.get(url, params)
    except:
        return HttpResponseServerError()

    data = r.json()["Data"]

    installed_by_year = dict()

    START_YEAR = 2019
    for entry in data:
        if not entry["InbetriebnahmeDatum"]:
            continue

        m = re.match("/Date\((-?\d*)\)/", entry["InbetriebnahmeDatum"])
        install_date = datetime.fromtimestamp(int(m.group(1)) / 1000)
        year = START_YEAR if install_date.year < START_YEAR else install_date.year

        if not year in installed_by_year:
            installed_by_year[year] = 0

        installed_by_year[year] += entry["Bruttoleistung"]

    current_year = date.today().year
    installed_accumulated = 0
    years = []
    installed = []
    for year, installed_in_year in sorted(installed_by_year.items()):
        if year == current_year:
            break
        installed_accumulated += round(installed_in_year)
        years.append(year)
        installed.append(installed_accumulated)

    data = json.dumps({"years": years, "installed": installed})
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


# Admin
class SelectCityView(ListView):
    model = City
    template_name = "admin/admin-city.html"
    ordering = "name"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Städte"
        return context


class CapEditView(DetailView, admin.ModelAdmin):
    model = City
    template_name = "admin/admin-cap.html"

    def get_context_data(self, **kwargs):
        groups = _get_task_groups(self.object)
        cap_checklist = _get_cap_checklist(self.object)
        administration_checklist = _get_administration_checklist(self.object)
        energy_plan_checklist = _get_energy_plan_checklist(self.object)

        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        context["city_id"] = str(self.object.pk)
        context["cap_checklist_id"] = (
            cap_checklist.pk if cap_checklist != None else None
        )
        context["administration_checklist_id"] = (
            administration_checklist.pk if administration_checklist != None else None
        )
        context["energy_plan_checklist_id"] = (
            energy_plan_checklist.pk if energy_plan_checklist != None else None
        )
        context["groups"] = groups
        return context


def move_task(request, pk):
    new_parent_pk = request.POST.get("new_parent_pk")
    task = Task.objects.get(pk=pk)
    new_parent = Task.objects.get(pk=new_parent_pk)
    position = request.POST.get("position")
    task.move(new_parent, position)
    return JsonResponse({"success": True})


#
# REST API views
#


class CityList(APIView):
    """
    List all cities.
    """

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class CityDetail(APIView):
    """
    Return a specific city.
    """

    def get(self, request, slug):
        try:
            city = City.objects.get(slug=slug)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CitySerializer(city)
        return Response(serializer.data)


class TasksByCity(APIView):
    """
    List all tasks of a city.
    """

    def get(self, request, slug):
        try:
            city = City.objects.get(slug=slug)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        city_id = city.id
        children = Task.get_root_nodes().filter(city=city_id)
        serializer = TaskSerializer(children, many=True)
        return Response(serializer.data)


#
# Temporary endpoints as dirty quick fix
# for Bundestreffen 2024 for filtering out drafts
#


class CityListWithoutDraftMode(APIView):
    """
    List all cities which are not in draft mode.
    """

    def get(self, request):
        cities = City.objects.all().exclude(draft_mode=True)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class TasksByCityWithoutDraftMode(APIView):
    """
    List all tasks of a city which are not in draft mode.
    """

    def get(self, request, slug):
        try:
            city = City.objects.get(slug=slug)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        city_id = city.id
        children = Task.get_root_nodes().filter(city=city_id, draft_mode=False)
        serializer = TaskWithoutDraftModeSerializer(children, many=True)
        return Response(serializer.data)
