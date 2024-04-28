# Generated by Django 4.2.9 on 2024-04-10 16:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cpmonitor", "0042_localgroup_logo_alter_localgroup_featured_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="administrationchecklist",
            options={
                "verbose_name": "Checkliste zu Verwaltungsstrukturen",
                "verbose_name_plural": "Checklisten zu Verwaltungsstrukturen",
            },
        ),
        migrations.AlterModelOptions(
            name="capchecklist",
            options={
                "verbose_name": "Checkliste zum KAP",
                "verbose_name_plural": "Checklisten zum KAP",
            },
        ),
        migrations.AlterModelOptions(
            name="energyplanchecklist",
            options={
                "verbose_name": "Checkliste zur Wärmeplanung",
                "verbose_name_plural": "Checklisten zur Wärmeplanung",
            },
        ),
    ]