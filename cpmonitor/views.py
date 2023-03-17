from django.http import Http404
from django.shortcuts import render
from .models import City, Task


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
    root_tasks = Task.get_root_nodes().filter(city=city)
    return render(
        request,
        "city.html",
        {
            "city": city,
            "tasks": root_tasks,
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
