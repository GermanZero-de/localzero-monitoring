from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView

from . import views

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
    path("admin/", admin.site.urls),
    path(
        "api/uploader/", views.markdown_uploader_view, name="markdown_uploader"
    ),  # needs to be before the martor urls, so that our image uplaoder and not the imgur uploader is used
    path("martor/", include("martor.urls")),
    path("accounts/", include("allauth.urls")),
    re_path(
        r"^invitations/accept-invite/(?P<key>\w+)/?$",
        views.AcceptInvite.as_view(),
        name="accept-invite",
    ),
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
    path(prefix_kommune + "<slug:city_slug>/massnahmen/", views.task_view, name="task"),
    path(
        prefix_kommune + "<slug:city_slug>/massnahmen/<path:task_slugs>/",
        views.task_view,
        name="task",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
