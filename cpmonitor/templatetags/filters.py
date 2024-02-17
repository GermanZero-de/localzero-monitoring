from urllib.parse import urlencode

from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse

from cpmonitor.models import ExecutionStatus, Task

register = template.Library()


@register.filter(name="task_execution_status_to_icon")
@stringfilter
def task_execution_status_to_icon(execution_status: str) -> str:
    match execution_status:
        case ExecutionStatus.UNKNOWN.name:
            return "progress-help"
        case ExecutionStatus.AS_PLANNED.name:
            return "progress"
        case ExecutionStatus.COMPLETE.name:
            return "circle-check"
        case ExecutionStatus.DELAYED.name:
            return "progress-alert"
        case ExecutionStatus.FAILED.name:
            return "circle-x"


@register.filter(name="task_children")
def task_children(group: Task):
    group_children = Task.get_tree(group)[1:]
    return group_children


@register.filter(name="depth_to_margin_left")
def depth_to_margin_left(task: Task):
    return "marginleft-" + str(task.depth - 2)


@register.simple_tag()
def admin_reverse(model, action, pk=None, **kwargs):
    reverse_str = f"admin:cpmonitor_{model}_{action}"
    if pk:
        url = reverse(reverse_str, args=[pk])
    else:
        url = reverse(reverse_str)
    if kwargs:
        query_str = urlencode(kwargs, safe="%")
        url += f"?{query_str}"
    return url
