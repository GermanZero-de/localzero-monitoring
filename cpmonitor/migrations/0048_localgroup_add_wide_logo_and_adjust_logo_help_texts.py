# Generated by Django 4.2.9 on 2024-11-06 21:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cpmonitor", "0047_rename_logo_localgroup_logo_square"),
    ]

    operations = [
        migrations.AddField(
            model_name="localgroup",
            name="logo_wide",
            field=models.ImageField(
                blank=True,
                help_text="\n            <p>Logo für die Hauptseite eurer Kommune.\n            Am besten nicht weiß, da es auf weißem Hintergrund angezeigt wird.</p>\n        ",
                upload_to="uploads/%Y/%m/%d/",
                verbose_name="breites Logo",
            ),
        ),
        migrations.AlterField(
            model_name="localgroup",
            name="featured_image",
            field=models.ImageField(
                blank=True,
                help_text="Mindestens 500 Pixel breit und 300 Pixel hoch.",
                upload_to="uploads/%Y/%m/%d/",
                verbose_name="Foto der Lokalgruppe",
            ),
        ),
        migrations.AlterField(
            model_name="localgroup",
            name="logo_square",
            field=models.ImageField(
                blank=True,
                help_text="\n            <p>Logo eurer Kommune für die Kommunenliste.\n            Am besten quadratisch und weiß auf transparent,\n            da es auf gelbem Hintergrund angezeigt wird.</p>\n        ",
                upload_to="uploads/%Y/%m/%d/",
                verbose_name="quadratisches Logo",
            ),
        ),
    ]
