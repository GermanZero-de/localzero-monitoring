from django.contrib import admin
from .models import City, Task
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class CityAdmin(admin.ModelAdmin):
    fields = ["zipcode", "name", "url", "introduction", "budget"]
    search_fields = ["zipcode", "name"]


class TaskAdmin(TreeAdmin):
    form = movenodeform_factory(Task)


admin.site.site_header = "LocalZero Monitoring"
admin.site.site_title = "LocalZero Monitoring"
admin.site.index_title = "Dateneingabe"


admin.site.register(City, CityAdmin)
admin.site.register(Task, TaskAdmin)
