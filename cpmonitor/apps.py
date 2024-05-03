from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class MyAdminConfig(AdminConfig):
    default_site = "cpmonitor.admin.AdminSite"


class CpmonitorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cpmonitor"
