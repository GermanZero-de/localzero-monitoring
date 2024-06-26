# Generated by Django 4.2.9 on 2024-04-12 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "cpmonitor",
            "0044_alter_administrationchecklist_climate_protection_management_exists_rationale_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="administrationchecklist",
            name="city",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="administration_checklist",
                to="cpmonitor.city",
                verbose_name="Stadt",
            ),
        ),
        migrations.AlterField(
            model_name="capchecklist",
            name="city",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="cap_checklist",
                to="cpmonitor.city",
                verbose_name="Stadt",
            ),
        ),
        migrations.AlterField(
            model_name="energyplanchecklist",
            name="city",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="energy_plan_checklist",
                to="cpmonitor.city",
                verbose_name="Stadt",
            ),
        ),
    ]
