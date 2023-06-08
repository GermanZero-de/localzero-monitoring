from collections import Counter
from datetime import date
import json
import os
import time
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from martor.utils import LazyEncoder

from .models import (
    City,
    ExecutionStatus,
    Task,
    CapChecklist,
    AdministrationChecklist,
)


def _show_drafts(request):
    return request.user.is_authenticated


def _calculate_summary(request, node):
    """calculate summarized status for a given node or a whole city"""

    statuses = {s.value: s for s in ExecutionStatus}
    if isinstance(node, City):
        subtasks = Task.objects.filter(city=node, numchild=0)
    else:
        subtasks = node.get_descendants().filter(numchild=0)
    if not _show_drafts(request):
        subtasks = subtasks.filter(draft_mode=False)

    subtasks_count = len(subtasks)
    status_counts = Counter([s.execution_status for s in subtasks])
    status_proportions = {
        s: round(c / subtasks_count * 100) for s, c in status_counts.items()
    }

    node.status_proportions = [
        (v, statuses[k].label, statuses[k].name)
        for k, v in sorted(status_proportions.items(), reverse=True)
    ]
    node.subtasks_count = subtasks_count
    node.complete_proportion = status_proportions.get(ExecutionStatus.COMPLETE, 0)
    node.incomplete_proportion = 100 - node.complete_proportion


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


# Our main page
def index_view(request):
    return render(request, "index.html", _get_base_context(request))


def city_view(request, city_slug):
    city = _get_cities(request, city_slug)
    if not city:
        raise Http404(f"Wir haben keine Daten zu der Kommune '{city_slug}'.")

    groups, tasks = _get_children(request, city)
    _calculate_summary(request, city)

    cap_checklist = _get_cap_checklist(city)
    cap_checklist_exists = cap_checklist != {}

    administration_checklist = _get_administration_checklist(city)
    administration_checklist_exists = administration_checklist != {}

    context = _get_base_context(request)
    context.update(
        {
            "city": city,
            "groups": groups,
            "tasks": tasks,
            "charts": city.charts.all,
            "cap_checklist_exists": cap_checklist_exists,
            "administration_checklist_exists": administration_checklist_exists,
            "asmt_admin": city.assessment_administration,
            "asmt_plan": city.assessment_action_plan,
            "asmt_status": city.assessment_status,
        }
    )

    if cap_checklist_exists:
        cap_checklist_total = len(cap_checklist)
        cap_checklist_number_fulfilled = list(cap_checklist.values()).count(True)
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
        administration_checklist_number_fulfilled = list(
            administration_checklist.values()
        ).count(True)
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
        days_gone_proportion = round(days_gone / days_total * 100)
        days_left_proportion = round(days_left / days_total * 100)
        context.update(
            {
                "days_gone": days_gone,
                "days_left": days_left,
                "days_gone_proportion": days_gone_proportion,
                "days_left_proportion": days_left_proportion,
            }
        )

    return render(request, "city.html", context)


def cap_checklist_view(request, city_slug):
    city = _get_cities(request, city_slug)
    if not city:
        raise Http404(f"Wir haben keine Daten zu der Kommune '{city_slug}'.")

    context = _get_base_context(request)
    context.update(
        {
            "city": city,
            "cap_checklist": _get_cap_checklist(city),
        }
    )
    return render(request, "cap_checklist.html", context)


def _get_cap_checklist(city) -> dict:
    try:
        checklist_items = city.cap_checklist._meta.get_fields()
    except CapChecklist.DoesNotExist:
        return {}

    checklist_items = [
        item for item in checklist_items if item.attname not in ["city_id", "id"]
    ]

    return {
        item.verbose_name: getattr(city.cap_checklist, item.attname)
        for item in checklist_items
    }


def administration_checklist_view(request, city_slug):
    city = _get_cities(request, city_slug)
    if not city:
        raise Http404(f"Wir haben keine Daten zu der Kommune '{city_slug}'.")

    context = _get_base_context(request)
    context.update(
        {
            "city": city,
            "administration_checklist": _get_administration_checklist(city),
        }
    )

    return render(request, "administration_checklist.html", context)


def _get_administration_checklist(city) -> dict:
    try:
        checklist_items = city.administration_checklist._meta.get_fields()
    except AdministrationChecklist.DoesNotExist:
        return {}

    checklist_items = [
        item for item in checklist_items if item.attname not in ["city_id", "id"]
    ]

    return {
        item.verbose_name: getattr(city.administration_checklist, item.attname)
        for item in checklist_items
    }


def _get_task(request, city, task_slugs):
    task = Task.objects.get(city=city, slugs=task_slugs)
    if task.draft_mode and not _show_drafts(request):
        raise Task.DoesNotExist()
    return task


def task_view(request, city_slug, task_slugs=None):
    city = _get_cities(request, city_slug)
    if not city:
        raise Http404(f"Wir haben keine Daten zu der Kommune '{city_slug}'.")

    if not task_slugs:
        groups, tasks = _get_children(request, city)

        return render(
            request,
            "taskgroup.html",
            {"city": city, "groups": groups, "tasks": tasks},
        )

    try:
        task: Task = _get_task(request, city, task_slugs)
    except Task.DoesNotExist:
        raise Http404(
            "Wir haben keine Daten zu dem Sektor / der Maßnahme '%s'." % task_slugs
        )

    context = _get_base_context(request)
    context.update({"city": city, "node": task})
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
    return render(request, "project.html", _get_base_context(request))


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
    img_url = os.path.join(settings.MEDIA_URL, def_path)

    data = json.dumps({"status": 200, "link": img_url, "name": image.name})
    return HttpResponse(data, content_type="application/json")
