# Generated by Django 4.1.7 on 2023-03-31 12:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cpmonitor", "0008_alter_task_execution_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="slugs",
            field=models.SlugField(
                editable=False, max_length=255, verbose_name="slugs"
            ),
        ),
        migrations.AddConstraint(
            model_name="task",
            constraint=models.UniqueConstraint(
                models.F("city"), models.F("slugs"), name="unique_urls"
            ),
        ),
    ]