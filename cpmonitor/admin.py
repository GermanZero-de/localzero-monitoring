from django.contrib import admin
from django.db import models
from django.http import HttpRequest, HttpResponseRedirect, QueryDict
from django.urls import reverse
from django.utils.html import format_html
from martor.widgets import AdminMartorWidget
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from cpmonitor.models import City, Task

_city_filter_query = "city__id__exact"
"""The query parameter used by the city filter."""


def _admin_url(model, type, city_id):
    """Reverse Django admin URL for a Model possibly filtered for one city.

    See https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#admin-reverse-urls

    Args:
        model (model.Model): The model for which to reverse the URL.
        type (str): "changelist", "add", "history", "delete", or "change".
        city_id (int|None): Primary key of city.

    Returns:
        str: URL including query string for filter.
    """
    app = model._meta.app_label
    name = model._meta.model_name
    base = reverse(f"admin:{app}_{name}_{type}")
    if city_id:
        return f"{base}?{_city_filter_query}={city_id}"
    else:
        return base


class CityAdmin(admin.ModelAdmin):
    list_display = ("zipcode", "name", "introduction", "edit_tasks")
    list_display_links = ("name",)
    ordering = ("name",)
    search_fields = ["zipcode", "name"]

    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }

    @admin.display(description="")
    def edit_tasks(self, city: City):
        """For each city, a link to the list (tree, actually) of Tasks for just that city."""
        list_url = _admin_url(Task, "changelist", city.id)
        return format_html('<a href="{}">KAP bearbeiten</a>', list_url)


class TaskAdmin(TreeAdmin):
    # ------ change list page ------
    change_list_template = "admin/task_changelist.html"

    @admin.display(description="Struktur")
    def structure(self, task: Task):
        """Additional read-only field showing the tree structure."""

        def add_parents(current: Task, substructure: str):
            parent = current.get_parent()
            if parent == None:
                return substructure
            else:
                return add_parents(parent, "%s --> %s" % (parent.title, substructure))

        return add_parents(task, task.title)

    list_display = ("title", "structure")
    form = movenodeform_factory(Task)

    list_filter = ("city",)

    def changelist_view(self, request):
        """Redirect to city changelist if no city filter is given."""
        city_id = request.GET.get(_city_filter_query)
        if not city_id:
            return HttpResponseRedirect(_admin_url(City, "changelist", None))
        else:
            return super().changelist_view(request)

    search_fields = ("title",)
    search_help_text = "Suche im Titel"

    # ------ add and change task page ------
    fields = (
        "city",
        "title",
        "summary",
        "description",
        "planned_start",
        "planned_completion",
        "responsible_organ",
        "plan_assessment",
        "execution_status",
        "execution_justification",
        "execution_completion",
        "actual_start",
        "actual_completion",
        "_position",
        "_ref_node_id",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("city",)
        else:
            return ()

    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }

    def get_changeform_initial_data(self, request: HttpRequest):
        """Prefill the city based on the filter preserved from the changelist view."""
        query_string = self.get_preserved_filters(request)
        filters = QueryDict(query_string).get("_changelist_filters")
        city_id = QueryDict(filters).get(_city_filter_query)
        return {"city": city_id}


admin.site.site_header = "LocalZero Monitoring"
admin.site.site_title = "LocalZero Monitoring"
admin.site.index_title = "Dateneingabe"

admin.site.register(City, CityAdmin)
admin.site.register(Task, TaskAdmin)
