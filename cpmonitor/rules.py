from django.contrib.auth.models import User
from django.db.models import Q, Model
import rules
from types import NoneType

from .models import City, Task, Chart, CapChecklist, AdministrationChecklist, LocalGroup

# All classes attached to a city (except Invitation) or a city ID.
CityType = (
    City | Task | Chart | CapChecklist | AdministrationChecklist | LocalGroup | int
)
CityOrNoneType = CityType | NoneType


_always_false_q: Q = Q(pk__in=[])
_always_true_q: Q = ~_always_false_q


def is_allowed_to_edit_q(user: User, model: Model | None) -> Q:
    """
    Return a Q object to filter objects to which a user has access.
    This may be used with `QuerySet.filter`, but also with `limit_choices_to`.
    """
    if not user.is_staff or not user.is_active:
        return _always_false_q
    if user.is_superuser:
        return _always_true_q
    if model == City:
        return Q(city_editors=user) | Q(city_admins=user)
    else:
        return Q(city__city_editors=user) | Q(city__city_admins=user)


def _get_city(object: CityOrNoneType) -> City | NoneType:
    "Helper to retrieve city from any object belonging to a city or a city ID."
    if isinstance(object, City):
        return object
    elif isinstance(object, int):
        return City.objects.filter(id=object).first()
    else:
        return getattr(object, "city", None)


@rules.predicate
def is_city_editor(user: User, object: CityOrNoneType) -> bool:
    "True, if user is city editor of the city object belongs to. False, if no object specified."
    if not user.is_staff or not user.is_active:
        return False
    city = _get_city(object)
    if isinstance(city, City):
        return city.city_editors.filter(pk=user.pk).exists()
    return False


@rules.predicate
def is_city_admin(user: User, object: CityOrNoneType) -> bool:
    "True, if user is city admin of the city object belongs to. False, if no object specified."
    if not user.is_staff or not user.is_active:
        return False
    city = _get_city(object)
    if isinstance(city, City):
        return city.city_admins.filter(pk=user.pk).exists()
    return False


@rules.predicate
def is_site_admin(user: User, object: CityOrNoneType) -> bool:
    "True, if user is site admin of the city object belongs to. False, if no object specified."
    if not user.is_superuser or not user.is_active:
        return False
    city = _get_city(object)
    if isinstance(city, City):
        return True
    return False


@rules.predicate
def no_object(user: User, object: CityOrNoneType) -> bool:
    "True if no object is specified and the user has access to the admin."
    if object is None and user.is_active and user.is_staff:
        return True
    return False


# Composed predicates:
is_allowed_to_edit = is_city_editor | is_city_admin | is_site_admin
is_allowed_to_change_city_users = is_city_admin | is_site_admin


# The actual permissions:

# Unfortunately, the admin sometimes asks for change permissions without specifying
# an object. Therefore, this case is handled with `no_object` below. Since the admin
# uses additional checks with the object, this is no breach of the restrictions.
# Note, that at some places the permissions have to be checked manually. See admin.py.

# Allow to view the admin at all:
rules.add_perm("cpmonitor", rules.always_true)

# City:
# Only add and change permissions are given to city editors and admins.
# Site admins are superusers and can change everything, anyway.
rules.add_perm("cpmonitor.view_city", is_allowed_to_edit)
rules.add_perm("cpmonitor.change_city", is_allowed_to_edit | no_object)

# Task:
rules.add_perm("cpmonitor.add_task", is_allowed_to_edit | no_object)
rules.add_perm("cpmonitor.view_task", is_allowed_to_edit)
rules.add_perm("cpmonitor.delete_task", is_allowed_to_edit)
rules.add_perm("cpmonitor.change_task", is_allowed_to_edit | no_object)

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

rules.add_perm("cpmonitor.add_energyplanchecklist", is_allowed_to_edit | no_object)
rules.add_perm("cpmonitor.view_energyplanchecklist", is_allowed_to_edit)
rules.add_perm("cpmonitor.delete_energyplanchecklist", is_allowed_to_edit)
rules.add_perm("cpmonitor.change_energyplanchecklist", is_allowed_to_edit | no_object)

rules.add_perm("cpmonitor.view_invitation", is_allowed_to_change_city_users | no_object)
rules.add_perm("cpmonitor.delete_invitation", is_allowed_to_change_city_users)
