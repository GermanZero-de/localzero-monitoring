from django.shortcuts import render
from .models import City, Task


# Our main page
def index(request):
    return render(
        request,
        "index.html",
        {
            "cities": City.objects.order_by("id"),
            "tasks": Task.objects.order_by("id"),
        },
    )
