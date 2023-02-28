from django.contrib import admin
from django.http import HttpRequest, HttpResponseRedirect, QueryDict
from django.utils.html import format_html
from django.urls import reverse
from cpmonitor.models import City, Task
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


_filter_string = "city__id__exact"


def _url(model, type, city_id):
    app = model._meta.app_label
    name = model._meta.model_name
    base = reverse(f"admin:{app}_{name}_{type}")
    if city_id:
        return f"{base}?{_filter_string}={city_id}"
    else:
        return base


class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "edit_tasks")
    search_fields = ["zipcode", "name"]

    @admin.display(description="")
    def edit_tasks(self, city: City):
        """For each city, link to Task changelist for just that city."""
        list_url = _url(Task, "changelist", city.id)
        return format_html('<a href="{}">KAP bearbeiten</a>', list_url)


class TaskAdmin(TreeAdmin):
    # ----- Changelist stuff ------

    change_list_template = "admin/task_changelist.html"

    @admin.display(description="Struktur")
    def structure(self, obj: Task):
        """Additional read-only field showing the tree structure."""

        def add_parent(o: Task, hdr: str):
            parent = o.get_parent()
            if parent == None:
                return hdr
            else:
                return add_parent(parent, "%s --> %s" % (parent.title, hdr))

        return add_parent(obj, obj.title)

    list_display = ("title", "structure")
    form = movenodeform_factory(Task)

    list_filter = ("city",)

    def changelist_view(self, request):
        """Redirect to city changelist if no city filter is given."""
        city_id = request.GET.get(_filter_string)
        if not city_id:
            return HttpResponseRedirect(_url(City, "changelist", None))
        else:
            return super().changelist_view(request)

    search_fields = ("title",)
    search_help_text = "Suche im Titel"

    # ----- Add / Change stuff -----

    def get_changeform_initial_data(self, request: HttpRequest):
        filters_qs = self.get_preserved_filters(request)
        print("Found filters: %s" % filters_qs)
        filters = QueryDict(filters_qs).get("_changelist_filters")
        city_id = QueryDict(filters).get(_filter_string)
        return {"city": city_id}

    # This does not work in conjunction with `get_changeform_initial_data`:
    # readonly_fields = ("city",)


admin.site.site_header = "LocalZero Monitoring"
admin.site.site_title = "LocalZero Monitoring"
admin.site.index_title = "Dateneingabe"

admin.site.register(City, CityAdmin)
admin.site.register(Task, TaskAdmin)
