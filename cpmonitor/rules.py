from django.contrib.auth.models import User
from django.db.models import Q, Model
import rules
from types import NoneType

from .models import City, Task, Chart

CityType = City | Task | Chart | int
CityOrNoneType = CityType | NoneType


def is_allowed_to_edit_q(user: User, model: Model) -> Q:
    if not user.is_staff or not user.is_active:
        return Q(pk__in=[])  # Always false -> Empty QuerySet
    if user.is_superuser:
        return ~Q(pk__in=[])  # Always true -> All objects
    if model == City:
        return Q(city_editors=user) | Q(city_admins=user)
    else:
        return Q(city__city_editors=user) | Q(city__city_admins=user)


def _get_city(object: CityOrNoneType) -> City | NoneType:
    if isinstance(object, City):
        return object
    elif isinstance(object, int):
        return City.objects.filter(id=object).first()
    else:
        return getattr(object, "city", None)


@rules.predicate
def is_city_editor(user: User, object: CityOrNoneType) -> bool:
    if not user.is_staff or not user.is_active:
        return False
    city = _get_city(object)
    if isinstance(city, City):
        return city.city_editors.filter(pk=user.pk).exists()
    return False


@rules.predicate
def is_city_admin(user: User, object: CityOrNoneType) -> bool:
    if not user.is_staff or not user.is_active:
        return False
    city = _get_city(object)
    if isinstance(city, City):
        return city.city_admins.filter(pk=user.pk).exists()
    return False


@rules.predicate
def is_site_admin(user: User, object: CityOrNoneType) -> bool:
    if not user.is_superuser or not user.is_active:
        return False
    city = _get_city(object)
    if isinstance(city, City):
        return True
    return False


@rules.predicate
def no_object(user: User, object: CityOrNoneType) -> bool:
    if object is None and user.is_active and user.is_staff:
        return True
    return False


is_allowed_to_edit = is_city_editor | is_city_admin | is_site_admin
is_allowed_to_change_city_users = is_city_admin | is_site_admin


# The actual permissions:

rules.add_perm("cpmonitor", rules.always_true)

# City:
# Only add and change permissions are given to city editors and admins.
# Site admins are superusers and can change everything, anyway.
rules.add_perm("cpmonitor.view_city", is_allowed_to_edit)
rules.add_perm("cpmonitor.change_city", is_allowed_to_edit | no_object)

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

rules.add_perm("cpmonitor.add_task", is_allowed_to_edit | no_object)
rules.add_perm("cpmonitor.view_task", is_allowed_to_edit)
rules.add_perm("cpmonitor.delete_task", is_allowed_to_edit)
rules.add_perm("cpmonitor.change_task", is_allowed_to_edit | no_object)

rules.add_perm("cpmonitor.view_invitation", is_allowed_to_change_city_users | no_object)
rules.add_perm("cpmonitor.delete_invitation", is_allowed_to_change_city_users)
