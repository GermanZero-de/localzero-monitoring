# Generated by Django 4.1.7 on 2023-04-20 14:28

from django.db import migrations, models
from django.utils.text import slugify

from ..models import Task as FullTask


def correct_slugs(apps, schema_editor):
    Task = apps.get_model("cpmonitor", "Task")
    db_alias = schema_editor.connection.alias
    for task in Task.objects.using(db_alias).all():
        task.__class__ = FullTask
        ancestor_titles = [a["title"] for a in task.get_ancestors().values("title")]
        task.__class__ = Task
        task.slugs = "/".join(slugify(t) for t in [*ancestor_titles, task.title])
        task.save()


class Migration(migrations.Migration):
    dependencies = [
        ("cpmonitor", "0009_alter_task_slugs_task_unique_urls"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="slugs",
            field=models.SlugField(
                editable=False, max_length=255, verbose_name="In der URL"
            ),
        ),
        migrations.RunPython(correct_slugs, migrations.RunPython.noop),
    ]
