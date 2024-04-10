from collections.abc import Sequence

from django.contrib import admin, messages
from django.db import models
from django.forms import TextInput
from django.forms.models import ErrorList
from django.http import HttpResponseRedirect, QueryDict
from django.http.request import HttpRequest
from django.urls import reverse, path
from django.utils.html import format_html
from martor.widgets import AdminMartorWidget
from rules.contrib.admin import ObjectPermissionsModelAdminMixin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm

from cpmonitor.views import SelectCityView, CapEditView
from . import rules, utils
from .models import (
    Chart,
    City,
    Task,
    AdministrationChecklist,
    LocalGroup,
    Invitation,
    EnergyPlanChecklist,
    CapChecklist,
)


class CapEditSite(admin.AdminSite):
    def get_urls(self):
        urlpatterns = super().get_urls()
        urlpatterns += [
            path("cap/", SelectCityView.as_view(), name="select-city"),
            path(
                "cap/<int:pk>/",
                CapEditView.as_view(),
                name="edit-cap",
            ),
        ]
        return urlpatterns


admin.site = CapEditSite()


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


class ChartInline(ObjectPermissionsModelAdminMixin, admin.StackedInline):
    model = Chart
    extra = 0

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "100"})},
        models.TextField: {"widget": AdminMartorWidget},
    }


class LocalGroupInline(ObjectPermissionsModelAdminMixin, admin.StackedInline):
    model = LocalGroup

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "100"})},
        models.TextField: {"widget": AdminMartorWidget},
    }


class InvitationInline(
    ObjectPermissionsModelAdminMixin, utils.ModelAdminRequestMixin, admin.StackedInline
):
    "Only show the invitation link and offer to delete them. Will be recreated upon next save."
    model = Invitation
    extra = 0
    fields = ("invitation_link",)
    readonly_fields = ("invitation_link",)

    @admin.display(description="Link")
    def invitation_link(self, invitation: Invitation):
        url = invitation.get_invite_url(self.get_request())
        role = str(invitation)
        return format_html(
            """
            <p>Diesen Link bitte nur an Menschen schicken, die mit dieser Rolle mitarbeiten sollen:</p>
            <p><a href="{}" target="_blank">{}</a></p>
            <p>Der Einladungslink ist so lange gültig, bis er gelöscht wird.</p>
            <p>Nach dem Löschen wird automatisch ein neuer Link erzeugt und hier angezeigt, wenn die
              Stadt das nächste Mal gespeichert wird.</p>
            <p>Sollte er nicht gleich sichtbar sein, bitte ein weiteres Mal speichern.</p>
            """,
            url,
            url,
        )


class ChecklistAdmin(ObjectPermissionsModelAdminMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("city",)
        else:
            return ()


class CityAdmin(ObjectPermissionsModelAdminMixin, admin.ModelAdmin):
    # ------ change list page ------
    list_display = ("zipcode", "name", "teaser", "edit_tasks")
    list_display_links = ("name",)
    ordering = ("name",)
    search_fields = ["zipcode", "name"]

    def get_queryset(self, request):
        "Restrict cities shown in changelist to those the user has access to."
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return qs
        return qs.filter(rules.is_allowed_to_edit_q(user, City)).distinct()

    @admin.display(description="")
    def edit_tasks(self, city: City):
        """For each city, a link to the list (tree, actually) of Tasks for just that city.

        This is the only entry point to reach the changelist for the tasks.
        """
        list_url = _admin_url(Task, "changelist", city.id)
        return format_html(
            '<a href="{}">Handlungsfelder / Maßnahmen bearbeiten</a>', list_url
        )

    # ------ change / add page ------
    save_on_top = True

    filter_horizontal = ["city_editors", "city_admins"]

    def get_readonly_fields(self, request: HttpRequest, obj=None) -> Sequence[str]:
        user = request.user
        result = []
        if not rules.is_allowed_to_change_city_users(user, obj):
            result.append("draft_mode")
            result.append("city_editors")
            result.append("city_admins")
        return result

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "170"})},
        models.TextField: {"widget": AdminMartorWidget},
    }

    inlines = [
        ChartInline,
        LocalGroupInline,
        InvitationInline,
    ]


class TaskForm(MoveNodeForm):
    """Fixed django-treebeard form to restrict the positions to move to the same city."""

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


class CityPermissionFilter(admin.RelatedFieldListFilter):
    """
    In the Task changelist (tree of tasks) on the right in the filter settings
    show only the cities for which the user has permission.
    By default, for a `list_filter` on a ForeignKey field, a RelatedFieldListFilter
    would be used.
    """

    def field_choices(self, field, request, model_admin):
        "Limit to cities the user is allowed to edit by using `limit_choices_to`."
        return field.get_choices(
            include_blank=False,
            ordering=self.field_admin_ordering(field, request, model_admin),
            limit_choices_to=rules.is_allowed_to_edit_q(request.user, City),
        )

    def has_output(self):
        "Show even a single possibility. Otherwise, the tasks will not be filtered."
        return len(self.lookup_choices) > 0


class TaskAdmin(ObjectPermissionsModelAdminMixin, TreeAdmin):
    # ------ change list page ------
    change_list_template = "admin/task_changelist.html"

    @admin.display(description="Öffentliche Seite")
    def slug_link(self, task: Task):
        """Additional link to the public page and also showing the slugs."""
        url = reverse(
            "task", kwargs={"city_slug": task.city.slug, "task_slugs": task.slugs}
        )
        return format_html('<a href="{}" target="_blank">{}</a>', url, task.slugs)

    list_display = ("title", "slug_link")
    form = movenodeform_factory(Task, TaskForm)

    list_filter = (("city", CityPermissionFilter),)

    def changelist_view(self, request):
        """Redirect to city changelist if no city filter is given."""
        city_id = request.GET.get(_city_filter_query)
        if city_id and rules.is_allowed_to_edit(request.user, int(city_id)):
            return super().changelist_view(request)

        msg = "Bitte eine Stadt auswählen, für die Handlungsfelder / Maßnahmen geändert werden sollen. Rechts davon 'Handlungsfelder / Maßnahmen bearbeiten' wählen."
        self.message_user(request, msg, messages.INFO)
        return HttpResponseRedirect(_admin_url(City, "changelist", None))

    search_fields = ("title",)
    search_help_text = "Suche im Titel"

    # ------ add and change task page ------
    save_on_top = True

    fields = (
        "city",
        "draft_mode",
        "frontpage",
        "title",
        "teaser",
        "description",
        "source",
        "planned_start",
        "planned_completion",
        "responsible_organ",
        "responsible_organ_explanation",
        "plan_assessment",
        "execution_status",
        "execution_justification",
        "supporting_ngos",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        "In the add form show only the cities the user has access to for the city the task belongs to."
        if db_field.name == "city":
            kwargs["queryset"] = City.objects.filter(
                rules.is_allowed_to_edit_q(request.user, City)
            ).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request: HttpRequest):
        """Prefill the city based on the filter preserved from the changelist view."""
        query_string = self.get_preserved_filters(request)
        filters = QueryDict(query_string).get("_changelist_filters")
        city_id = QueryDict(filters).get(_city_filter_query)
        return {
            "city": city_id,
            "_position": request.GET.get("position"),
            "_ref_node_id": request.GET.get("relative_to"),
        }

    def add_view(self, request, form_url="", extra_context=None):
        "Only show the add form if a city is selected to which the user has access."
        query_string = self.get_preserved_filters(request)
        filters = QueryDict(query_string).get("_changelist_filters")
        city_id = QueryDict(filters).get(_city_filter_query)
        if city_id and rules.is_allowed_to_edit(request.user, int(city_id)):
            return super().add_view(request, form_url, extra_context)

        msg = "Bitte eine Stadt auswählen, für die Handlungsfelder / Maßnahmen geändert werden sollen. Rechts davon 'Handlungsfelder / Maßnahmen bearbeiten' wählen."
        self.message_user(request, msg, messages.INFO)
        return HttpResponseRedirect(_admin_url(City, "changelist", None))


admin.site.site_header = "LocalZero Monitoring"
admin.site.site_title = "LocalZero Monitoring"
admin.site.index_title = "Dateneingabe"

admin.site.register(City, CityAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(CapChecklist, ChecklistAdmin)
admin.site.register(AdministrationChecklist, ChecklistAdmin)
admin.site.register(EnergyPlanChecklist, ChecklistAdmin)
