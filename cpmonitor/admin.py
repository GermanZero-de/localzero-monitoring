from django.contrib import admin
from .models import City, Task, Sector, TaskCategory

from django.contrib.auth.models import User, Group

class TaskInline(admin.TabularInline):
    model=Task
    extra = 2
    

class CityAdmin(admin.ModelAdmin):
    fields = ['zipcode', 'name', 'url', 'info']
    inlines = [TaskInline]
    search_fields =['zipcode','name']
    

admin.site.site_header='LocalZero Monitoring'
admin.site.site_title='LocalZero Monitoring'
admin.site.index_title='Dateneingabe'


admin.site.register(City,CityAdmin)
admin.site.register(Task)

admin.site.register(Sector)
admin.site.register(TaskCategory)

