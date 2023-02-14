from django.contrib import admin
from .models import City, Task
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class CityAdmin(admin.ModelAdmin):
    fields = ["zipcode", "name", "url", "introduction", "budget"]
    search_fields = ["zipcode", "name"]


class TaskAdmin(TreeAdmin):
    list_filter = ("city__name",)
    form = movenodeform_factory(Task)


admin.site.site_header = "LocalZero Monitoring"
admin.site.site_title = "LocalZero Monitoring"
admin.site.index_title = "Dateneingabe"

admin.site.register(City, CityAdmin)
admin.site.register(Task, TaskAdmin)

# # May be used to inspect the internals of treebeard.mp_tree.MP_Node
# class TaskInternalsAdmin(admin.ModelAdmin):
#     list_filter = ("city__name",)
# class TaskInternals(Task):
#     class Meta:
#         proxy = True
# admin.site.register(TaskInternals, TaskInternalsAdmin)
