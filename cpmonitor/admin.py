from django.contrib import admin
from .models import City, Task
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin


class TaskInline(OrderedTabularInline):
    model = Task
    fields = (
        "parent",
        "title",
        "description",
        "planned_start",
        "planned_completion",
        "state",
        "justification",
        "completion",
        "order",
        "move_up_down_links",
    )
    readonly_fields = (
        "order",
        "move_up_down_links",
    )
    ordering = ("order",)
    extra = 2


class CityAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    fields = ["zipcode", "name", "url", "introduction", "budget"]
    inlines = [TaskInline]
    search_fields = ["zipcode", "name"]


admin.site.site_header = "LocalZero Monitoring"
admin.site.site_title = "LocalZero Monitoring"
admin.site.index_title = "Dateneingabe"


admin.site.register(City, CityAdmin)
admin.site.register(Task)
