import pytest

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client
from itertools import chain
from pytest_django.asserts import (
    assertTemplateUsed,
    assertTemplateNotUsed,
    assertContains,
    assertNotContains,
)


@pytest.fixture(scope="session")
def permissions_db(django_db_setup, django_db_blocker):
    "Fixture to load the test data fixture for permissions tests."
    with django_db_blocker.unblock():
        call_command("loaddata", "permissions")


def _fields_from_form(form):
    "Retrieve the fields from all fieldsets of a form."
    list_of_lists = list(map(lambda fieldset: fieldset[1]["fields"], form.fieldsets))
    return chain(*list_of_lists)


# Some utilities for logging in


def _login(client: Client, django_user_model: User, username: str):
    "Helper for logging in as an existing user present in the database."
    user = django_user_model.objects.get(username=username)
    client.force_login(user)


@pytest.fixture
def unprivileged_client(permissions_db, client: Client, django_user_model: User):
    "Client fixture with data loaded and unprivileged user logged in."
    _login(client, django_user_model, "christian")  # password: derehring
    return client


@pytest.fixture
def site_admin_client(permissions_db, client: Client, django_user_model: User):
    "Client fixture with data loaded and site admin user logged in."
    _login(client, django_user_model, "admin")  # password: password
    return client


@pytest.fixture
def city_admin_client(permissions_db, client: Client, django_user_model: User):
    "Client fixture with data loaded and city admin user logged in."
    _login(client, django_user_model, "sarah")  # passowrd: diebrosetti
    return client


@pytest.fixture
def city_editor_client(permissions_db, client: Client, django_user_model: User):
    "Client fixture with data loaded and city editor user logged in."
    _login(client, django_user_model, "heinz")  # password: derstrunk
    return client


# Tests for plain login to admin site


def test_admin_login_should_fail_fail_for_non_existing_user(
    permissions_db, client: Client, db
):
    client.login(username="asdf", password="ghjk")
    response = client.get("/admin/")
    assertTemplateNotUsed(response, "admin/index.html")


def test_admin_login_should_fail_for_unprivileged_user(unprivileged_client: Client):
    response = unprivileged_client.get("/admin/")
    assertTemplateNotUsed(response, "admin/index.html")


def test_admin_login_should_succeed_for_site_admin(site_admin_client: Client):
    response = site_admin_client.get("/admin/")
    assertTemplateUsed(response, "admin/index.html")


def test_admin_login_should_succeed_for_city_admin(city_admin_client: Client):
    response = city_admin_client.get("/admin/")
    assertTemplateUsed(response, "admin/index.html")


def test_admin_login_should_succeed_for_city_editor(city_editor_client: Client):
    response = city_editor_client.get("/admin/")
    assertTemplateUsed(response, "admin/index.html")


# City changelist


def test_city_changelist_should_contain_all_cities_and_add_for_site_admin(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/city/")
    assertTemplateUsed(response, "admin/change_list.html")
    result_list = response.context["results"]
    assert isinstance(result_list, list) and len(result_list) == 3
    assertContains(response, "Beispielstadt")
    assertContains(response, "Mitallem")
    assertContains(response, "Ohnenix")

    assertContains(response, "Kommune hinzufügen")


def test_city_changelist_should_only_contain_one_city_and_no_add_for_city_admin(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/city/")
    assertTemplateUsed(response, "admin/change_list.html")
    result_list = response.context["results"]
    assert isinstance(result_list, list) and len(result_list) == 1
    assertContains(response, "Beispielstadt")
    assertNotContains(response, "Mitallem")

    assertNotContains(response, "Kommune hinzufügen")


def test_city_changelist_should_only_contain_one_city_and_no_add_for_city_editor(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/city/")
    assertTemplateUsed(response, "admin/change_list.html")
    result_list = response.context["results"]
    assert isinstance(result_list, list) and len(result_list) == 1
    assertContains(response, "Beispielstadt")
    assertNotContains(response, "Mitallem")

    assertNotContains(response, "Kommune hinzufügen")


# City change form


def test_city_editor_should_not_be_allowed_to_access_to_another_city(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/city/2/change/")

    assert response.status_code == 302
    assert response.url == "/admin/"


def test_city_admin_should_not_be_allowed_to_access_to_another_city(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/city/2/change/")

    assert response.status_code == 302
    assert response.url == "/admin/"


def test_site_admin_should_not_be_allowed_to_access_to_another_city(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/city/2/change/")

    assert response.status_code == 200
    assertTemplateUsed(response, "admin/change_form.html")


def test_city_editor_should_not_be_allowed_to_delete_add_and_change_editors_and_admins(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/city/1/change/")

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert not response.context["show_delete_link"]
    assert not response.context["show_save_and_add_another"]

    adminform = response.context["adminform"]
    fields = _fields_from_form(adminform)
    assert "draft_mode" in fields
    assert "city_editors" in fields
    assert "city_admins" in fields
    assert "draft_mode" in adminform.readonly_fields
    assert "city_editors" in adminform.readonly_fields
    assert "city_admins" in adminform.readonly_fields


def test_city_admin_should_not_be_allowed_to_delete_add_but_to_change_editors_and_admins(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/city/1/change/")

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert not response.context["show_delete_link"]
    assert not response.context["show_save_and_add_another"]

    adminform = response.context["adminform"]
    fields = _fields_from_form(adminform)
    assert "draft_mode" in fields
    assert "city_editors" in fields
    assert "city_admins" in fields
    assert not "draft_mode" in adminform.readonly_fields
    assert not "city_editors" in adminform.readonly_fields
    assert not "city_admins" in adminform.readonly_fields


def test_site_admin_should_be_allowed_to_delete_add_and_to_change_editors_and_admins(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/city/1/change/")

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert response.context["show_delete_link"]
    assert response.context["show_save_and_add_another"]

    adminform = response.context["adminform"]
    fields = _fields_from_form(adminform)
    assert "draft_mode" in fields
    assert "city_editors" in fields
    assert "city_admins" in fields
    assert not "draft_mode" in adminform.readonly_fields
    assert not "city_editors" in adminform.readonly_fields
    assert not "city_admins" in adminform.readonly_fields


def test_city_editor_should_be_allowed_to_modify_inlines(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/city/1/change/")

    formsets = response.context["inline_admin_formsets"]

    verbose_names = list(map(lambda formset: formset.opts.verbose_name, formsets))

    assert "Diagramm" in verbose_names
    assert "Lokalgruppe" in verbose_names
    assert len(formsets) == 2

    for formset in formsets:
        assert formset.has_view_permission
        assert formset.has_add_permission
        assert formset.has_change_permission
        assert formset.has_delete_permission


def test_city_admin_should_be_allowed_to_modify_inlines(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/city/1/change/")

    formsets = response.context["inline_admin_formsets"]

    verbose_names = list(map(lambda formset: formset.opts.verbose_name, formsets))

    assert "Diagramm" in verbose_names
    assert "Lokalgruppe" in verbose_names
    assert "Einladungslink" in verbose_names
    assert len(formsets) == 3

    for formset in formsets:
        assert formset.has_view_permission
        if formset.opts.verbose_name != "Einladungslink":
            assert formset.has_add_permission
            assert formset.has_change_permission
        assert formset.has_delete_permission


def test_site_admin_should_be_allowed_to_modify_inlines(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/city/1/change/")

    formsets = response.context["inline_admin_formsets"]

    verbose_names = list(map(lambda formset: formset.opts.verbose_name, formsets))

    assert "Diagramm" in verbose_names
    assert "Lokalgruppe" in verbose_names
    assert "Einladungslink" in verbose_names
    assert len(formsets) == 3

    for formset in formsets:
        assert formset.has_view_permission
        assert formset.has_add_permission
        assert formset.has_change_permission
        assert formset.has_delete_permission


# Task changelist


def test_city_editor_should_not_be_allowed_to_view_tasks_of_nonexistent_city(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/task/?city__id__exact=9")

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_city_admin_should_not_be_allowed_to_view_tasks_of_nonexistent_city(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/task/?city__id__exact=9")

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_site_admin_should_not_be_allowed_to_view_tasks_of_nonexistent_city(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/task/?city__id__exact=9")

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_city_editor_should_not_be_allowed_to_view_tasks_of_other_city(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/task/?city__id__exact=3")

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_city_admin_should_not_be_allowed_to_view_tasks_of_other_city(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/task/?city__id__exact=3")

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_site_admin_should_not_be_allowed_to_view_tasks_of_other_city(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/task/?city__id__exact=3")

    assert response.status_code == 200
    assertTemplateUsed(response, "admin/change_list.html")


def test_city_editor_should_be_allowed_to_view_and_add_tasks_of_city(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/task/?city__id__exact=1")
    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_list.html")

    assertContains(response, "Maßnahme hinzufügen")

    assertContains(response, "/beispielstadt/massnahmen/")
    assertNotContains(response, "/mitallem/massnahmen/")


def test_city_admin_should_be_allowed_to_view_and_add_tasks_of_city(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/task/?city__id__exact=1")
    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_list.html")

    assertContains(response, "Maßnahme hinzufügen")

    assertContains(response, "/beispielstadt/massnahmen/")
    assertNotContains(response, "/mitallem/massnahmen/")


def test_site_admin_should_be_allowed_to_view_and_add_tasks_of_city(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/task/?city__id__exact=1")
    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_list.html")

    assertContains(response, "Maßnahme hinzufügen")

    assertContains(response, "/beispielstadt/massnahmen/")
    assertNotContains(response, "/mitallem/massnahmen/")


def test_city_editor_should_only_see_his_city_in_filter_list(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/task/?city__id__exact=1")

    filter_choices = list(
        map(lambda choice: choice["display"], response.context["choices"])
    )
    assert "12345 Beispielstadt" in filter_choices
    assert not "99999 Mitallem" in filter_choices


def test_city_admin_should_only_see_his_city_in_filter_list(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/task/?city__id__exact=1")

    filter_choices = list(
        map(lambda choice: choice["display"], response.context["choices"])
    )
    assert "12345 Beispielstadt" in filter_choices
    assert not "99999 Mitallem" in filter_choices


def test_site_admin_should_see_all_cities_in_filter_list(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/task/?city__id__exact=1")

    filter_choices = list(
        map(lambda choice: choice["display"], response.context["choices"])
    )
    assert "12345 Beispielstadt" in filter_choices
    assert "99999 Mitallem" in filter_choices


# Task add form


def test_city_editor_should_not_be_allowed_to_add_task_without_city(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/task/add/")

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_city_admin_should_not_be_allowed_to_add_task_without_city(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/task/add/")

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_site_admin_should_not_be_allowed_to_add_task_without_city(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/task/add/")

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_city_editor_should_not_be_allowed_to_add_task_for_nonexistent_city(
    city_editor_client: Client,
):
    response = city_editor_client.get(
        "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D9"
    )

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_city_admin_should_not_be_allowed_to_add_task_for_nonexistent_city(
    city_admin_client: Client,
):
    response = city_admin_client.get(
        "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D9"
    )

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_site_admin_should_not_be_allowed_to_add_task_for_nonexistent_city(
    site_admin_client: Client,
):
    response = site_admin_client.get(
        "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D9"
    )

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_city_editor_should_not_be_allowed_to_add_task_for_other_city(
    city_editor_client: Client,
):
    response = city_editor_client.get(
        "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D3"
    )

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_city_admin_should_not_be_allowed_to_add_task_for_other_city(
    city_admin_client: Client,
):
    response = city_admin_client.get(
        "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D3"
    )

    assert response.status_code == 302
    assert response.url == "/admin/cpmonitor/city/"


def test_site_admin_should_be_allowed_to_add_task_for_other_city(
    site_admin_client: Client,
):
    response = site_admin_client.get(
        "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D3"
    )

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert response.context["show_save_and_add_another"]

    assertContains(response, "99999 Mitallem")


def city_choices(adminform):
    for fieldset in adminform:
        for fieldline in fieldset:
            for field in fieldline:
                field_form = field.field.field
                if field_form.label == "City":
                    choices = list(field_form.choices)
                    for choice in choices:
                        yield choice[1]


def test_city_editor_should_be_allowed_to_add_task_only_for_his_city(
    city_editor_client: Client,
):
    response = city_editor_client.get(
        "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D1"
    )

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert response.context["show_save_and_add_another"]

    adminform = response.context["adminform"]
    cities = list(city_choices(adminform))
    assert "12345 Beispielstadt" in cities
    assert not "99999 Mitallem" in cities


def test_city_admin_should_be_allowed_to_add_task_only_for_his_city(
    city_admin_client: Client,
):
    response = city_admin_client.get(
        "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D1"
    )

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert response.context["show_save_and_add_another"]

    adminform = response.context["adminform"]
    cities = list(city_choices(adminform))
    assert "12345 Beispielstadt" in cities
    assert not "99999 Mitallem" in cities


def test_site_admin_should_be_allowed_to_add_task_for_all_cities(
    site_admin_client: Client,
):
    response = site_admin_client.get(
        "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D1"
    )

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert response.context["show_save_and_add_another"]

    adminform = response.context["adminform"]
    cities = list(city_choices(adminform))
    assert "12345 Beispielstadt" in cities
    assert "99999 Mitallem" in cities


# Task change form


def test_city_editor_should_be_allowed_to_change_task_of_city(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/task/1/change/")

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert response.context["show_delete_link"]
    assert response.context["show_save_and_add_another"]

    adminform = response.context["adminform"]
    fields = _fields_from_form(adminform)
    assert "city" in fields
    assert "teaser" in fields
    assert "city" in adminform.readonly_fields
    assert not "teaser" in adminform.readonly_fields

    assertContains(response, "12345 Beispielstadt")


def test_city_admin_should_be_allowed_to_change_task_of_city(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/task/1/change/")

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert response.context["show_delete_link"]
    assert response.context["show_save_and_add_another"]

    adminform = response.context["adminform"]
    fields = _fields_from_form(adminform)
    assert "city" in fields
    assert "teaser" in fields
    assert "city" in adminform.readonly_fields
    assert not "teaser" in adminform.readonly_fields

    assertContains(response, "12345 Beispielstadt")


def test_site_admin_should_be_allowed_to_change_task_of_city(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/task/1/change/")

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert response.context["show_delete_link"]
    assert response.context["show_save_and_add_another"]

    adminform = response.context["adminform"]
    fields = _fields_from_form(adminform)
    assert "city" in fields
    assert "teaser" in fields
    assert "city" in adminform.readonly_fields
    assert not "teaser" in adminform.readonly_fields

    assertContains(response, "12345 Beispielstadt")


def test_city_editor_should_not_be_allowed_to_change_task_of_other_city(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/task/27/change/")

    assert response.status_code == 403


def test_city_admin_should_not_be_allowed_to_change_task_of_other_city(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/task/27/change/")

    assert response.status_code == 403


def test_site_admin_should_not_be_allowed_to_change_task_of_other_city(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/task/27/change/")

    assert response.status_code == 200


# Invitation links

city_admin_key = "ercizfqjtsqbv5xap4uvlkpswjivqnjiephfxdbhjett8jah0z0ynnfpqrqxjcjg"
city_editor_key = "lypvs6fb6qxk8ylskkckwp3g3djilpsiiunm1fuz68rdwg1emuwhnsuxexpbgjel"


def test_city_editor_should_not_be_able_to_see_invitation_links(
    city_editor_client: Client,
):
    response = city_editor_client.get("/admin/cpmonitor/city/1/change/")

    assertNotContains(response, city_admin_key)
    assertNotContains(response, city_editor_key)


def test_city_admin_should_be_able_to_see_invitation_links(
    city_admin_client: Client,
):
    response = city_admin_client.get("/admin/cpmonitor/city/1/change/")

    assertContains(response, city_admin_key)
    assertContains(response, city_editor_key)


def test_site_admin_should_be_able_to_see_invitation_links(
    site_admin_client: Client,
):
    response = site_admin_client.get("/admin/cpmonitor/city/1/change/")

    assertContains(response, city_admin_key)
    assertContains(response, city_editor_key)


# This is poor-mans parametrization, since pytest-django does not support it:


def _assert_not_logged_in(client: Client):
    response = client.get("/admin/", follow=True)
    assertTemplateNotUsed(response, "admin/index.html")


def _assert_logged_in(client: Client):
    response = client.get("/admin/", follow=True)
    assertTemplateUsed(response, "admin/index.html")


def _register_with_registration_link(key, client: Client):
    _assert_not_logged_in(client)

    response = client.get(f"/invitations/accept-invite/{key}")
    assert response.status_code == 302
    assert response.url == "/accounts/signup/"

    response = client.get(f"/invitations/accept-invite/{key}", follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "account/signup.html")
    assertNotContains(response, "Fehler")

    response = client.post(
        "/accounts/signup/",
        {
            "username": "kirstin",
            "email": "",
            "password1": "diewarnke",
            "password2": "diewarnkr",
        },
    )
    assert response.status_code == 200
    assertTemplateUsed(response, "account/signup.html")
    assertContains(response, "Fehler")

    response = client.post(
        "/accounts/signup/",
        {
            "username": "kirstin",
            "email": "",
            "password1": "diewarnke",
            "password2": "diewarnke",
        },
    )
    assert response.status_code == 302
    assert response.url == "/admin/"

    _assert_logged_in(client)

    client.logout()


def _login_with_new_account(client: Client):
    _assert_not_logged_in(client)

    client.login(username="kirstin", password="diewarnke")

    _assert_logged_in(client)


def _assert_city_changelist_contains_only_allowed(client: Client):
    response = client.get("/admin/cpmonitor/city/")
    assertTemplateUsed(response, "admin/change_list.html")
    result_list = response.context["results"]
    assert isinstance(result_list, list) and len(result_list) == 1
    assertContains(response, "Beispielstadt")
    assertNotContains(response, "Mitallem")

    assertNotContains(response, "Kommune hinzufügen")


def _assert_other_city_cannot_be_changed(client: Client):
    response = client.get("/admin/cpmonitor/city/2/change/")
    assert response.status_code == 302
    assert response.url == "/admin/"


def _assert_city_can_be_changed(client: Client):
    response = client.get("/admin/cpmonitor/city/1/change/")

    assert response.status_code == 200

    assertTemplateUsed(response, "admin/change_form.html")

    assert not response.context["show_delete_link"]
    assert not response.context["show_save_and_add_another"]


def test_can_register_with_city_editor_registration_link(
    permissions_db, db, client: Client
):
    _register_with_registration_link(city_editor_key, client)
    _login_with_new_account(client)
    _assert_city_changelist_contains_only_allowed(client)
    _assert_other_city_cannot_be_changed(client)
    _assert_city_can_be_changed(client)

    response = client.get("/admin/cpmonitor/city/1/change/")
    adminform = response.context["adminform"]
    assert "draft_mode" in adminform.readonly_fields
    assert "city_editors" in adminform.readonly_fields
    assert "city_admins" in adminform.readonly_fields
    assertNotContains(response, city_admin_key)
    assertNotContains(response, city_editor_key)


def test_can_register_with_city_admin_registration_link(
    permissions_db, db, client: Client
):
    _register_with_registration_link(city_admin_key, client)
    _login_with_new_account(client)
    _assert_city_changelist_contains_only_allowed(client)
    _assert_other_city_cannot_be_changed(client)
    _assert_city_can_be_changed(client)

    response = client.get("/admin/cpmonitor/city/1/change/")
    adminform = response.context["adminform"]
    assert not "draft_mode" in adminform.readonly_fields
    assert not "city_editors" in adminform.readonly_fields
    assert not "city_admins" in adminform.readonly_fields
    assertContains(response, city_admin_key)
    assertContains(response, city_editor_key)


def test_city_editor_should_be_able_to_accept_invitation_link_for_city_admin(
    city_editor_client: Client,
):
    response = city_editor_client.get(
        f"/invitations/accept-invite/{city_admin_key}", follow=True
    )
    assertTemplateUsed(response, "admin/index.html")
    assertContains(
        response,
        "Nutzer heinz ist eingeloggt und ist jetzt auch Kommunen-Administrator von Beispielstadt",
    )

    response = city_editor_client.get("/admin/cpmonitor/city/1/change/")
    assertTemplateUsed(response, "admin/change_form.html")

    adminform = response.context["adminform"]
    fields = _fields_from_form(adminform)
    assert "draft_mode" in fields
    assert "city_editors" in fields
    assert "city_admins" in fields
    assert not "draft_mode" in adminform.readonly_fields
    assert not "city_editors" in adminform.readonly_fields
    assert not "city_admins" in adminform.readonly_fields
