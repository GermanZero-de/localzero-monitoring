# Generated by Django 4.1.7 on 2023-08-01 17:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cpmonitor", "0024_task_responsible_organ_explanation_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="responsible_organ",
            field=models.CharField(
                blank=True,
                help_text="Name oder gebräuchliche Abkürzung des verantwortlichen Gremiums oder Behörde",
                max_length=200,
                verbose_name="Verantwortliches Organ",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="responsible_organ_explanation",
            field=models.TextField(
                blank=True,
                help_text="\n            <p>Ausgeschriebener Name, falls eine Abkürzung für das verantwortliche Organ verwendet wurde.</p>\n            <p>Eventuell Ansprechperson oder Kontaktdaten, wenn diese öffentlich zugänglich sind.</p>\n            <p>Gegebenenfalls eine Begründung, warum es an diesem Organ hängt.</p>\n        ",
                verbose_name="Erklärungstext zum verantwortlichen Organ",
            ),
        ),
    ]
