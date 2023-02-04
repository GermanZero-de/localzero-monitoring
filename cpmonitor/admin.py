from django.contrib import admin
from .models import City, Task, Sector, TaskCategory

admin.site.register(City)
admin.site.register(Task)

admin.site.register(Sector)
admin.site.register(TaskCategory)