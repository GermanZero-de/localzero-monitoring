# Generated by Django 4.1.7 on 2023-07-02 13:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "cpmonitor",
            "0023_task_frontpage",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="responsible_organ_explanation",
            field=models.TextField(
                blank=True,
                help_text="\n            <p>Eventuell Ansprechperson oder Kontaktdaten, wenn diese öffentlich zugänglich sind.</p>\n            <p>Gegebenenfalls eine Begründung, warum es an diesem Organ hängt.</p>\n        ",
                verbose_name="Erklärungstext zum verantwortlichen Organ",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="responsible_organ",
            field=models.CharField(
                blank=True, max_length=200, verbose_name="Verantwortliches Organ"
            ),
        ),
    ]
