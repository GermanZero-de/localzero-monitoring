from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url=settings.STATIC_URL + "favicon.png", permanent=True),
    ),
    path("admin/", admin.site.urls),
    path("martor/", include("martor.urls")),
    path("api/uploader/", views.markdown_uploader_view, name="markdown_uploader"),
    path("", views.index, name="index"),
    path("<slug:city_slug>/", views.city_view, name="city"),
    path(
        "<slug:city_slug>/kap_checkliste/",
        views.cap_checklist_view,
        name="cap_checklist",
    ),
    path(
        "<slug:city_slug>/verwaltungsstrukturen_checkliste/",
        views.administration_checklist_view,
        name="administration_checklist",
    ),
    path("<slug:city_slug>/massnahmen/", views.task_view, name="task"),
    path(
        "<slug:city_slug>/massnahmen/<path:task_slugs>/", views.task_view, name="task"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
