# Generated by Django 4.1.7 on 2023-05-17 15:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cpmonitor", "0015_capchecklist_delete_checklistclimateactionplan"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="capchecklist",
            options={"verbose_name": "KAP Checkliste"},
        ),
        migrations.RenameField(
            model_name="capchecklist",
            old_name="KAP Checkliste",
            new_name="city",
        ),
    ]
