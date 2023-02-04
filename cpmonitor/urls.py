from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [path("admin/", admin.site.urls), path("", views.index, name="index")]
