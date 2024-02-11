from django import template
from django.template.defaultfilters import stringfilter

from cpmonitor.models import ExecutionStatus

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
def task_children(group):
    return group.get_children()
