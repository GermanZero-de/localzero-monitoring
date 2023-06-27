from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.forms.models import ErrorList
from django.http import HttpRequest, HttpResponseRedirect, QueryDict
from django.urls import reverse
from django.utils.html import format_html
from martor.widgets import AdminMartorWidget
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm

from .models import Chart, City, Task, CapChecklist, AdministrationChecklist, LocalGroup

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


class ChartInline(admin.StackedInline):
    model = Chart
    extra = 0

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "100"})},
        models.TextField: {"widget": AdminMartorWidget},
    }


class CapChecklistInline(admin.TabularInline):
    model = CapChecklist


class AdministrationChecklistInline(admin.TabularInline):
    model = AdministrationChecklist


class LocalGroupInline(admin.StackedInline):
    model = LocalGroup

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "100"})},
        models.TextField: {"widget": AdminMartorWidget},
    }


class CityAdmin(admin.ModelAdmin):
    list_display = ("zipcode", "name", "teaser", "edit_tasks")
    list_display_links = ("name",)
    ordering = ("name",)
    search_fields = ["zipcode", "name"]

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "170"})},
        models.TextField: {"widget": AdminMartorWidget},
    }

    @admin.display(description="")
    def edit_tasks(self, city: City):
        """For each city, a link to the list (tree, actually) of Tasks for just that city."""
        list_url = _admin_url(Task, "changelist", city.id)
        return format_html('<a href="{}">KAP bearbeiten</a>', list_url)

    inlines = [
        ChartInline,
        LocalGroupInline,
        CapChecklistInline,
        AdministrationChecklistInline,
    ]


class TaskForm(MoveNodeForm):
    """Restrict the positions to move to the same city."""

    def __init__(
        self,
        data=None,
        files=None,
        auto_id="id_%s",
        prefix=None,
        initial=None,
        error_class=ErrorList,
        label_suffix=":",
        empty_permitted=False,
        instance=None,
        **kwargs,
    ):
        """Extract the city from 3 different sources."""
        if isinstance(instance, Task):
            self.city = instance.city.id
        elif isinstance(initial, dict) and "city" in initial:
            self.city = initial["city"]
        elif isinstance(data, dict) and "city" in data:
            self.city = data["city"][0]
        super().__init__(
            data=data,
            files=files,
            auto_id=auto_id,
            prefix=prefix,
            initial=initial,
            error_class=error_class,
            label_suffix=label_suffix,
            empty_permitted=empty_permitted,
            instance=instance,
            **kwargs,
        )

    def mk_dropdown_tree(self, model, for_node=None):
        """
        Overriding to filter for the city.
        Class method is overridden as an instance method to access self.city.
        """
        options = [(None, "Oberste Ebene")]
        for node in model.get_root_nodes().filter(city=self.city):
            self.__class__.add_subtree(for_node, node, options)
        return options

    def clean(self):
        """Prepare uniqueness validation of `slugs` in case position or title changed in form.

        This only updates `slugs` according to new parents `slugs` and title.
        The actual validation is done by `validate_constraints` in the model.
        The descendant's `slugs` are corrected during `instance.save()`.
        """

        # Based on treebeard.forms.MoveNodeForm._clean_cleaned_data():
        reference_node_id = None
        if "_ref_node_id" in self.cleaned_data:
            if self.cleaned_data["_ref_node_id"] != "0":
                reference_node_id = self.cleaned_data["_ref_node_id"]
                if reference_node_id.isdigit():
                    reference_node_id = int(reference_node_id)
        reference_node = None
        if reference_node_id:
            reference_node = self._meta.model.objects.get(pk=reference_node_id)
        position_type = self.cleaned_data["_position"]

        title = self.cleaned_data["title"]

        self.instance.slugs = self.instance.get_slugs_for_move(
            reference_node, position_type, title
        )

        return super().clean()


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

    @admin.display(description="Public page")
    def slug_link(self, task: Task):
        """Additional link to the public page and also showing the slugs."""
        url = reverse(
            "task", kwargs={"city_slug": task.city.slug, "task_slugs": task.slugs}
        )
        return format_html('<a href="{}" target="_blank">{}</a>', url, task.slugs)

    list_display = ("title", "structure", "slug_link")
    form = movenodeform_factory(Task, TaskForm)

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
        "draft_mode",
        "title",
        "teaser",
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
        models.CharField: {"widget": TextInput(attrs={"size": "170"})},
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
