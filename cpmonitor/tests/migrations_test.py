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
    which cannot be used, since it uses `django.apps.apps` and we need to use `old_state.apps`.
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


def test_complete_migrations_from_0006(migrator: Migrator) -> None:
    """
    Tests all migrations starting at 0006 work in both ways.

    Test starting from migration 0006 loading meaningful data and continue
    to the end and back, thereby testing all future migrations.
    """

    # Prepare DB up to migration 00006 before execution_status refactoring
    old_state = migrator.apply_initial_migration((app_name, "0006_alter_task_city"))

    # Read a complete data set for that model version
    read_fixture("complete_0006", app_name, old_state.apps)

    # Complete migration all the way to the current state
    migrator.reset()

    # Check some data
    assert Task.objects.get(pk=5).execution_status == 8

    # Migrate backward to migration 00006 before the execution_status refactoring
    back_state = migrator.apply_tested_migration((app_name, "0006_alter_task_city"))

    # Check some data (back conversion in migration 0008)
    back_Task = back_state.apps.get_model(app_name, "Task")
    assert back_Task.objects.get(pk=5).execution_assessment == 5
    assert back_Task.objects.get(pk=5).execution_progress == 0


def test_migration_0007(migrator: Migrator) -> None:
    """Test the status conversion of migration 0007 in both directions."""

    # Prepare DB up to migration 00006 before execution_status refactoring
    old_state = migrator.apply_initial_migration((app_name, "0006_alter_task_city"))

    # Read a complete data set for that model version
    read_fixture("complete_0006", app_name, old_state.apps)

    # Check the execution_status values (for comparison with backward conversion below)
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

    # Migrate to migration 0007
    new_state = migrator.apply_tested_migration(
        (app_name, "0007_rename_to_execution_status_and_more")
    )

    # Check that `execution_status` is set correctly for some Tasks
    new_Task = new_state.apps.get_model(app_name, "Task")
    assert new_Task.objects.get(pk=1).execution_status == 0
    assert new_Task.objects.get(pk=2).execution_status == 2
    assert new_Task.objects.get(pk=3).execution_status == 4
    assert new_Task.objects.get(pk=4).execution_status == 6
    assert new_Task.objects.get(pk=5).execution_status == 8

    # Migrate backward to migration 00006 before the execution_status refactoring
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


def test_migration_0007_by_hand(migrator: Migrator) -> None:
    """Test the status conversion of migration 0007 in both directions without fixture."""

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

    # Migrate to migration 0007
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

    # Migrate back to migration 0006
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

    migrator.reset()
