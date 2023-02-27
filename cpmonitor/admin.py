from django.contrib import admin
from django.http import QueryDict
from django.urls import reverse, path
from django.utils.html import format_html
from .models import City, Task
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "edit_tasks")
    search_fields = ["zipcode", "name"]

    def _view_prefix(self):
        return "%s_%s" % (
            self.model._meta.app_label,
            Task._meta.model_name,
        )

    @admin.display(description="")
    def edit_tasks(self, city: City):
        prefix = self._view_prefix()
        list_url = reverse("admin:%s_changelist" % prefix, kwargs={"citypk": city.pk})
        return format_html('<a href="{}">KAP bearbeiten</a>', list_url)

    def get_urls(self):
        urls = super().get_urls()

        def wrap(view):
            return self.admin_site.admin_view(view)

        prefix = self._view_prefix()
        my_urls = [
            path(
                "<int:citypk>/task/",
                wrap(self.task_changelist),
                name="%s_changelist" % prefix,
            ),
            path(
                "<int:citypk>/task/add/",
                wrap(self.task_add),
                name="%s_add" % prefix,
            ),
        ]
        return my_urls + urls

    def __init__(self, model, admin_site):
        self.task_admins: dict[str, TaskAdmin] = {}
        super().__init__(model, admin_site)

    def task_changelist(self, request, citypk):
        if citypk not in self.task_admins:
            self.task_admins[citypk] = TaskAdmin(Task, self.admin_site, citypk)
        task_admin = self.task_admins[citypk]
        return task_admin.changelist_view(request)

    def task_add(self, request, citypk):
        if citypk not in self.task_admins:
            self.task_admins[citypk] = TaskAdmin(Task.self.admin_site, citypk)
        task_admin = self.task_admins[citypk]
        return task_admin.add_view(request)


class TaskAdmin(TreeAdmin):
    save_on_top = True
    list_display = ("task", "title", "structure")
    list_editable = ("title",)
    # readonly_fields = ("city",)
    search_fields = ("city__name", "structure")
    search_help_text = "Enter city or part of title"
    form = movenodeform_factory(Task)

    def __init__(self, model, admin_site, citypk=None):
        self.citypk = citypk
        super().__init__(model, admin_site)

    def get_queryset(self, request):
        if self.citypk:
            return super().get_queryset(request).filter(city__pk=self.citypk)
        else:
            return super().get_queryset(request)

    def get_changeform_initial_data(self, request):
        filters = self.get_preserved_filters(request)
        filterDict = QueryDict(filters)
        return {"description": str(self.citypk)}

    @admin.display(description="Maßnahme")
    def task(self, obj: Task):
        return obj.title

    @admin.display(description="Struktur")
    def structure(self, obj: Task):
        def add_parent(o: Task, hdr: str):
            parent = o.get_parent()
            if parent == None:
                return hdr
            else:
                return add_parent(parent, "%s   -->   %s" % (parent.title, hdr))

        return add_parent(obj, obj.title)


admin.site.site_header = "LocalZero Monitoring"
admin.site.site_title = "LocalZero Monitoring"
admin.site.index_title = "Dateneingabe"

admin.site.register(City, CityAdmin)
# admin.site.register(Task, TaskAdmin)
