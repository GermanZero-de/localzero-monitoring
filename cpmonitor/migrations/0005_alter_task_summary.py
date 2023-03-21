# Generated by Django 4.1.7 on 2023-03-21 20:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cpmonitor", "0004_city_slug_task_slugs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="summary",
            field=models.TextField(
                blank=True,
                help_text="\n            <p>Kann Beschreibung, Bewertung und Umsetzungsstand enthalten.</p>\n            <p>Kann in einer Übersicht mehrerer Sektoren / Maßnahmen dargestellt werden.</p>\n            <p>Deswegen möglichst kurz und ohne Formatierungen. Fett, Kursiv, Links, etc. sind okay.</p>\n        ",
                verbose_name="Kurztext",
            ),
        ),
    ]
