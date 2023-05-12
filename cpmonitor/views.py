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
    ChecklistClimateActionPlan,
    ChecklistSustainabilityArchitectureInAdministration,
)


def _calculate_summary(node):
    """calculate summarized status for a give node or a whole city"""

    statuses = {s.value: s for s in ExecutionStatus}
    if isinstance(node, City):
        subtasks = [
            t
            for r in Task.get_root_nodes().filter(city=node)
            for t in r.get_descendants().filter(numchild=0)
        ]
    else:
        subtasks = node.get_descendants().filter(numchild=0)

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
    node.completed_proportion = status_proportions.get(ExecutionStatus.COMPLETE, 0)


def _get_children(city, node=None):
    if not node:
        children = Task.get_root_nodes().filter(city=city)
    else:
        children = node.get_children()

    groups = children.filter(numchild__gt=0)
    tasks = children.filter(numchild=0)
    for group in groups:
        _calculate_summary(group)

    return groups, tasks


# Our main page
def index(request):
    return render(
        request,
        "index.html",
        {
            "cities": City.objects.order_by("id"),
        },
    )


def city(request, city_slug):
    try:
        city = City.objects.get(slug=city_slug)
    except City.DoesNotExist:
        raise Http404(f"Wir haben keine Daten zu der Kommune '{city_slug}'.")
    groups, tasks = _get_children(city)
    _calculate_summary(city)

    context = {
        "city": city,
        "groups": groups,
        "tasks": tasks,
        "charts": city.charts.all,
        "checklist_climate_action_plan": get_checklist_climate_action_plan(city),
        "checklist_sustainability_architecture_in_administration": get_checklist_sustainability_architecture_in_administration(
            city
        ),
        "asmt_admin": city.assessment_administration,
        "asmt_plan": city.assessment_action_plan,
        "asmt_status": city.assessment_status,
    }

    if city.resolution_date and city.target_year:
        target_date = date(city.target_year, 12, 31)
        days_total = (target_date - city.resolution_date).days + 1
        days_gone = (date.today() - city.resolution_date).days
        days_left = days_total - days_gone
        days_gone_proportion = round(days_gone / days_total * 100)
        context.update(
            {
                "days_gone": days_gone,
                "days_left": days_left,
                "days_gone_proportion": days_gone_proportion,
            }
        )

    return render(request, "city.html", context)


def get_checklist_climate_action_plan(city):
    checklist_climate_action_plan = {}

    try:
        checklist_items = city.checklist_climate_action_plan._meta.get_fields()
    except ChecklistClimateActionPlan.DoesNotExist:
        return checklist_climate_action_plan

    checklist_items = filter(
        lambda a: a.attname != "KAP Checkliste_id" and a.attname != "id",
        checklist_items,
    )
    for checklist_item in checklist_items:
        checklist_climate_action_plan[checklist_item.verbose_name] = getattr(
            city.checklist_climate_action_plan, checklist_item.attname
        )
    return checklist_climate_action_plan


def get_checklist_sustainability_architecture_in_administration(city):
    checklist_sustainability_architecture = {}

    try:
        checklist_items = (
            city.checklist_sustainability_architecture_in_administration._meta.get_fields()
        )
    except ChecklistSustainabilityArchitectureInAdministration.DoesNotExist:
        return checklist_sustainability_architecture

    checklist_id = "Nachhaltigkeitsarchitektur in der Verwaltung Checkliste_id"
    checklist_items = filter(
        lambda a: a.attname != checklist_id and a.attname != "id",
        checklist_items,
    )
    for checklist_item in checklist_items:
        checklist_sustainability_architecture[checklist_item.verbose_name] = getattr(
            city.checklist_sustainability_architecture_in_administration,
            checklist_item.attname,
        )
    return checklist_sustainability_architecture


def task(request, city_slug, task_slugs):
    try:
        city = City.objects.get(slug=city_slug)
    except City.DoesNotExist:
        raise Http404("Wir haben keine Daten zu der Kommune '%s'." % city_slug)
    try:
        task: Task = Task.objects.get(city=city, slugs=task_slugs)
    except Task.DoesNotExist:
        raise Http404(
            "Wir haben keine Daten zu dem Sektor / der Maßnahme '%s'." % task_slugs
        )

    if task.is_leaf():
        return render(
            request,
            "task.html",
            {"city": city, "node": task},
        )
    else:
        groups, tasks = _get_children(city, task)

        return render(
            request,
            "group.html",
            {"city": city, "node": task, "groups": groups, "tasks": tasks},
        )


@login_required
def markdown_uploader(request):
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
