import json
import os
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

from .models import City, ExecutionStatus, Task


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
    groups = Task.get_root_nodes().filter(city=city)
    for group in groups:
        tasks = group.get_descendants().filter(numchild=0)
        total = len(tasks)
        statuses = {s.value: s for s in ExecutionStatus}
        group.statuses = {}
        for task in tasks:
            status = task.execution_status
            group.statuses[status] = group.statuses.get(status, 0) + round(100 / total)

        group.statuses = [
            (v, statuses[k].label, statuses[k].name)
            for k, v in sorted(group.statuses.items(), reverse=True)
        ]
        group.total = total

    return render(
        request,
        "city.html",
        {
            "city": city,
            "groups": groups,
        },
    )


def task(request, city_slug, task_slugs):
    try:
        city = City.objects.get(slug=city_slug)
    except City.DoesNotExist:
        raise Http404("Wir haben keine Daten zu der Kommune '%s'." % city_slug)
    try:
        task: Task = Task.objects.get(slugs=task_slugs)
    except City.DoesNotExist:
        raise Http404(
            "Wir haben keine Daten zu dem Sektor / der Maßnahme '%s'." % task_slugs
        )
    subtasks = task.get_children()

    return render(
        request,
        "task.html",
        {
            "city": city,
            "task": task,
            "subtasks": subtasks,
        },
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
    tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
    def_path = default_storage.save(tmp_file, ContentFile(image.read()))
    img_url = os.path.join(settings.MEDIA_URL, def_path)

    data = json.dumps({"status": 200, "link": img_url, "name": image.name})
    return HttpResponse(data, content_type="application/json")
