import os
import json
from django.apps import apps
from django.apps.registry import Apps
from django.db.models import ManyToOneRel
from django_test_migrations.migrator import Migrator

from cpmonitor.models import Task

app_name = "cpmonitor"


def read_fixture(fixture_name: str, app_name: str, migration_state_apps: Apps):
    """
    Reads data from a JSON fixture file of the given application into a given applications state.

    This is a drastically simplified version of `django.core.management` "loaddata" command,
    which cannot be used, since it uses `django.apps.apps` and we need to use `migration_state_apps`.
    `django.apps.apps.get_model()` returns classes from the current model while
    `migration_state_apps.get_model()` returns classes matching the state of the model at the
    migration state.
    """
    app_path = apps.get_app_config(app_name).path
    fixture_path = os.path.join(app_path, "fixtures", fixture_name + ".json")

    with open(fixture_path, "rb") as f:
        json_list = json.load(f)
        for json_obj in json_list:
            Model = migration_state_apps.get_model(json_obj["model"])
            data = {}
            if "pk" in json_obj:
                data[Model._meta.pk.attname] = Model._meta.pk.to_python(
                    json_obj.get("pk")
                )
            for field_name, field_value in json_obj["fields"].items():
                field = Model._meta.get_field(field_name)
                if field.remote_field:
                    if not isinstance(field.remote_field, ManyToOneRel):
                        raise Exception(
                            "Field type not supported by this migration test."
                        )
                    remote_name = field.remote_field.field_name
                    remote_field = field.remote_field.model._meta.get_field(remote_name)
                    data[field.attname] = remote_field.to_python(field_value)
                else:
                    data[field.name] = field.to_python(field_value)
            Model.objects.create(**data)


def test_should_succeed_when_migrating_complete_data_set_from_0006_to_current_and_back(
    migrator: Migrator,
) -> None:
    """
    Tests all migrations starting at 0006 work in both ways.

    The main expectation of this test is, that the migrations are applied without error.
    The assertions are just there to verify that they were applied.

    Test starting from migration 0006, loading meaningful data which covers
    most possible cases at the time, and continuing to the end and back,
    thereby also testing all future migrations.
    """

    old_state = migrator.apply_initial_migration((app_name, "0006_alter_task_city"))

    read_fixture("complete_0006", app_name, old_state.apps)

    # Complete migration all the way to the current state. `apply_tested_migration` does not work here.
    migrator.reset()

    # Verify the conversion in migration 0007 was applied.
    assert Task.objects.get(pk=5).execution_status == 8

    back_state = migrator.apply_tested_migration((app_name, "0006_alter_task_city"))

    # Verify the back-conversion in migration 0007, again.
    back_Task = back_state.apps.get_model(app_name, "Task")
    assert back_Task.objects.get(pk=5).execution_assessment == 5
    assert back_Task.objects.get(pk=5).execution_progress == 0


def test_should_convert_status_correctly_when_migrating_0007_and_back(
    migrator: Migrator,
) -> None:
    """Test the status conversion of migration 0007 in both directions.

    This loads test data from a fixture file and thereby covers most
    possible cases, but might be more fragile.
    See comment for `test_migration_0007_by_hand`.
    """

    old_state = migrator.apply_initial_migration((app_name, "0006_alter_task_city"))

    read_fixture("complete_0006", app_name, old_state.apps)

    # Just for comparison with backward conversion below.
    old_Task = old_state.apps.get_model(app_name, "Task")
    assert old_Task.objects.get(pk=1).execution_assessment == 0
    assert old_Task.objects.get(pk=1).execution_progress == 0
    assert old_Task.objects.get(pk=2).execution_assessment == 2
    assert old_Task.objects.get(pk=2).execution_progress == 2
    assert old_Task.objects.get(pk=3).execution_assessment == 2
    assert old_Task.objects.get(pk=3).execution_progress == 4
    assert old_Task.objects.get(pk=4).execution_assessment == 3
    assert old_Task.objects.get(pk=4).execution_progress == 2
    assert old_Task.objects.get(pk=5).execution_assessment == 5
    assert old_Task.objects.get(pk=5).execution_progress == 4

    new_state = migrator.apply_tested_migration(
        (app_name, "0007_rename_to_execution_status_and_more")
    )

    new_Task = new_state.apps.get_model(app_name, "Task")
    assert new_Task.objects.get(pk=1).execution_status == 0
    assert new_Task.objects.get(pk=2).execution_status == 2
    assert new_Task.objects.get(pk=3).execution_status == 4
    assert new_Task.objects.get(pk=4).execution_status == 6
    assert new_Task.objects.get(pk=5).execution_status == 8

    back_state = migrator.apply_tested_migration((app_name, "0006_alter_task_city"))

    # Check the backward conversion values
    back_Task = back_state.apps.get_model(app_name, "Task")
    assert back_Task.objects.get(pk=1).execution_assessment == 0
    assert back_Task.objects.get(pk=1).execution_progress == 0
    assert back_Task.objects.get(pk=2).execution_assessment == 2
    assert back_Task.objects.get(pk=2).execution_progress == 2
    assert back_Task.objects.get(pk=3).execution_assessment == 2
    assert back_Task.objects.get(pk=3).execution_progress == 4
    assert back_Task.objects.get(pk=4).execution_assessment == 3
    assert back_Task.objects.get(pk=4).execution_progress == 2
    assert back_Task.objects.get(pk=5).execution_assessment == 5
    assert back_Task.objects.get(pk=5).execution_progress == 0


def test_should_convert_status_correctly_when_migrating_0007_and_back_by_hand(
    migrator: Migrator,
) -> None:
    """Test the status conversion of migration 0007 in both directions without fixture.

    This is very similar to `test_migration_0007` and probably too redundant.
    Currently, it is not clear, which one is easier to maintain. If one of the
    two makes problems, it is probably best just do remove it.
    """

    old_state = migrator.apply_initial_migration((app_name, "0006_alter_task_city"))

    old_City = old_state.apps.get_model(app_name, "City")
    testburg = old_City.objects.create(name="Testburg", zipcode="12345")

    old_Task = old_state.apps.get_model(app_name, "Task")
    energie = old_Task.objects.create(
        title="Energie",
        city=testburg,
        execution_assessment=2,
        execution_progress=4,
        # Make sure, all constraints are satisfied, manually:
        depth=1,
        path="0001",
        slugs="a",
    )
    verkehr = old_Task.objects.create(
        title="Verkehr",
        city=testburg,
        execution_assessment=5,
        execution_progress=4,
        # Make sure, all constraints are satisfied, manually:
        depth=1,
        path="0002",
        slugs="b",
    )

    new_state = migrator.apply_tested_migration(
        (app_name, "0007_rename_to_execution_status_and_more")
    )

    new_City = new_state.apps.get_model(app_name, "City")
    assert new_City.objects.count() == 1
    new_testburg = new_City.objects.get(name=testburg.name)

    new_Task = new_state.apps.get_model(app_name, "Task")
    assert new_Task.objects.count() == 2
    new_energie = new_Task.objects.get(city=new_testburg, title=energie.title)
    assert new_energie.execution_status == 4
    new_verkehr = new_Task.objects.get(city=new_testburg, title=verkehr.title)
    assert new_verkehr.execution_status == 8

    back_state = migrator.apply_tested_migration((app_name, "0006_alter_task_city"))

    back_City = back_state.apps.get_model(app_name, "City")
    assert back_City.objects.count() == 1
    back_testburg = back_City.objects.get(name=testburg.name)

    back_Task = back_state.apps.get_model(app_name, "Task")
    assert back_Task.objects.count() == 2
    back_energie = back_Task.objects.get(city=back_testburg, title=energie.title)
    assert back_energie.execution_assessment == 2
    assert back_energie.execution_progress == 4
    back_verkehr = back_Task.objects.get(city=back_testburg, title=verkehr.title)
    assert back_verkehr.execution_assessment == 5
    assert back_verkehr.execution_progress == 0
