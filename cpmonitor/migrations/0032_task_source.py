# Generated by Django 4.1.7 on 2023-11-16 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cpmonitor", "0031_resize_and_reorder_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="source",
            field=models.IntegerField(
                choices=[(0, "KAP"), (1, "Vorschlag")],
                default=0,
                help_text="Stammt dieses Handlungsfeld / diese Maßnahme aus dem bereits vorhandenen Klimaaktions-Plan oder handelt es sich hierbei um einen Vorschlag eures Lokalteams? Hinweis: Bei Handlungsfeldern hat dieses Feld aktuell keine Auswirkungen auf die Darstellung und wird ignoriert.",
                verbose_name="KAP oder eigener Vorschlag?",
            ),
        ),
    ]