from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import path, re_path, include
from django.views.generic import RedirectView

from . import views
from .admin import admin_site
from .views import SelectCityView, CapEditView, move_task

urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url=settings.STATIC_URL + "favicon.svg", permanent=True),
    ),
    path("admin/cap/", login_required(SelectCityView.as_view()), name="select-city"),
    path(
        "admin/cap/<int:pk>/",
        login_required(CapEditView.as_view()),
        name="edit-cap",
    ),
    path("admin/cap/task/move/<int:pk>/", login_required(move_task)),
    path("admin/", admin_site.urls),
    path("api/uploader/", views.markdown_uploader_view, name="markdown_uploader"),
    path("api/mstr/<slug:municipality_key>", views.mstr_view, name="mstr"),
    path("martor/", include("martor.urls")),
    path("accounts/", include("allauth.urls")),
    re_path(
        r"^invitations/accept-invite/(?P<key>\w+)/?$",
        views.AcceptInvite.as_view(),
        name="accept-invite",
    ),
    path("api/uploader/", views.markdown_uploader_view, name="markdown_uploader"),
    # Declare frontend task URLs so treebeard can reverse them.
    # The dummy "view" returned here is never shown because nginx requests this from the frontend app instead!
    path(
        "<slug:city_slug>/massnahmen/<path:task_slugs>/",
        lambda _: HttpResponse(
            "this is where nginx proxies the task page of the frontend app when deployed"
        ),
        name="task",
    ),
    # Declare frontend index URL so it can be reversed by django when city admin or editor invitations are accepted
    path(
        "",
        lambda _: HttpResponse(
            "this is where nginx proxies the index page of the frontend app when deployed"
        ),
        name="index",
    ),
    # REST API urls
    #
    # Use accept header "application/json" to get json
    #
    path("api/cities", views.CityList.as_view()),
    path("api/cities/<str:slug>", views.CityDetail.as_view()),
    path("api/cities/<str:slug>/tasks", views.TasksByCity.as_view()),
    path("api/tasks/top", views.TasksTop.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
