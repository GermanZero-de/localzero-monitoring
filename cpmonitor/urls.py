from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include
from django.views.generic import RedirectView

from . import views
from .admin import admin_site
from .views import SelectCityView, CapEditView, move_task

prefix_kommune = ""

urlpatterns = [
    path("projekt/", views.project_view, name="project"),
    path("impressum/", views.impressum_view, name="impressum"),
    path("datenschutz/", views.datenschutz_view, name="datenschutz"),
    path("ueber-uns/", views.ueber_uns_view, name="ueber-uns"),
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
    path("", views.index_view, name="index"),
    path(prefix_kommune + "<slug:city_slug>/", views.city_view, name="city"),
    path(
        prefix_kommune + "<slug:city_slug>/lokalgruppe/",
        views.local_group_view,
        name="local_group",
    ),
    path(
        prefix_kommune + "<slug:city_slug>/kap_checkliste/",
        views.cap_checklist_view,
        name="cap_checklist",
    ),
    path(
        prefix_kommune + "<slug:city_slug>/verwaltungsstrukturen_checkliste/",
        views.administration_checklist_view,
        name="administration_checklist",
    ),
    path(
        prefix_kommune + "<slug:city_slug>/waermeplanung_checkliste/",
        views.energy_plan_checklist_view,
        name="energy_plan_checklist",
    ),
    path(prefix_kommune + "<slug:city_slug>/massnahmen/", views.task_view, name="task"),
    path(
        prefix_kommune + "<slug:city_slug>/massnahmen/<path:task_slugs>/",
        views.task_view,
        name="task",
    ),
    #
    # REST API urls
    #
    # Use accept header "application/json" to get json
    #
    path("api/cities", views.CityList.as_view()),
    path("api/cities/<str:slug>", views.CityDetail.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
