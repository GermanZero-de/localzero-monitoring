from django.shortcuts import render


# Our main page
def index(request):
    return render(request, "index.html", {})
