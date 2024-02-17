from django.forms import ModelForm

from cpmonitor.models import Task


class TaskForm(ModelForm):
    class Meta:
        fields = [
            "path",
            "depth",
        ]
        model = Task
