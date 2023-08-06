from django.contrib.auth.models import User
from django.db.models import QuerySet, Q
import rules
from types import NoneType
from typing import TypeVar

from .models import City, Task, Chart

CityObject = City | Task | Chart | NoneType
T = TypeVar("T", City, Task)


def filter_editable(user: User, qs: QuerySet[T]) -> QuerySet[T]:
    if qs.model == City:
        return qs.filter(Q(city_editors=user) | Q(city_admins=user))
    else:
        return qs.filter(Q(city__city_editors=user) | Q(city__city_admins=user))


def _get_city(object: CityObject) -> City | NoneType:
    # print(object)
    if isinstance(object, City):
        return object
    else:
        return getattr(object, "city", None)


@rules.predicate
def is_city_editor(user: User, object: CityObject) -> bool:
    city = _get_city(object)
    if isinstance(city, City):
        return city.city_editors.filter(pk=user.pk).exists()
    else:
        return False


@rules.predicate
def is_city_admin(user: User, object: CityObject) -> bool:
    city = _get_city(object)
    if isinstance(city, City):
        return city.city_admins.filter(pk=user.pk).exists()
    else:
        return False


@rules.predicate
def is_site_admin(user: User, object: CityObject) -> bool:
    return user.is_superuser


@rules.predicate
def no_object(user: User, object: CityObject) -> bool:
    if object is None:
        return True


is_allowed_to_edit = is_city_editor | is_city_admin | is_site_admin
is_allowed_to_change_site_editors = is_city_admin | is_site_admin
is_allowed_to_change_site_admins = is_city_admin | is_site_admin


# The actual permissions:

# City:
# Only add and change permissions are given to city editors and admins.
# Site admins are superusers and can change everything, anyway.
rules.add_perm("cpmonitor.view_city", is_allowed_to_edit)
rules.add_perm("cpmonitor.change_city", is_allowed_to_edit)

# Inlines in city mask:
# For some reason, "change" is requested with "None" once by inlines.
rules.add_perm("cpmonitor.add_chart", is_allowed_to_edit | no_object)
rules.add_perm("cpmonitor.view_chart", is_allowed_to_edit)
rules.add_perm("cpmonitor.delete_chart", is_allowed_to_edit)
rules.add_perm("cpmonitor.change_chart", is_allowed_to_edit | no_object)

rules.add_perm("cpmonitor.add_localgroup", is_allowed_to_edit | no_object)
rules.add_perm("cpmonitor.view_localgroup", is_allowed_to_edit)
rules.add_perm("cpmonitor.delete_localgroup", is_allowed_to_edit)
rules.add_perm("cpmonitor.change_localgroup", is_allowed_to_edit | no_object)

rules.add_perm("cpmonitor.add_administrationchecklist", is_allowed_to_edit | no_object)
rules.add_perm("cpmonitor.view_administrationchecklist", is_allowed_to_edit)
rules.add_perm("cpmonitor.delete_administrationchecklist", is_allowed_to_edit)
rules.add_perm(
    "cpmonitor.change_administrationchecklist", is_allowed_to_edit | no_object
)

rules.add_perm("cpmonitor.add_capchecklist", is_allowed_to_edit | no_object)
rules.add_perm("cpmonitor.view_capchecklist", is_allowed_to_edit)
rules.add_perm("cpmonitor.delete_capchecklist", is_allowed_to_edit)
rules.add_perm("cpmonitor.change_capchecklist", is_allowed_to_edit | no_object)

# TODO: This currently does not ensure that tasks are not added to other cities:
rules.add_perm("cpmonitor.add_task", is_allowed_to_edit | no_object)
rules.add_perm("cpmonitor.view_task", is_allowed_to_edit)
rules.add_perm("cpmonitor.delete_task", is_allowed_to_edit)
rules.add_perm("cpmonitor.change_task", is_allowed_to_edit)
