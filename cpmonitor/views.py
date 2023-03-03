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


def city(request, city_name):
    return render(
        request,
        "city.html",
        {
            "city": City.objects.filter(name=city_name).get(),
            # TODO: only return tasks for this city so we needn't filter in frontend
            "tasks": Task.objects.order_by("id"),
        },
    )
