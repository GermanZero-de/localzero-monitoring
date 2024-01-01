# Generated by Django 4.2.7 on 2024-01-01 19:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cpmonitor", "0035_alter_localgroup_featured_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="administrationchecklist",
            name="intersectoral_concepts_exists",
            field=models.BooleanField(
                default=False,
                help_text="Sektorenübergreifende Konzepte sind zum Beispiel Kimaanpassungs- , Konzepte der Städtebauförderung oder Quartierskonzepte. Diese Konzepte betrachten Maßnahmen, die über mehrere Sektoren gehen, das Quartierskonzept betrachtet zum Beispiel die Gebäudesanierung, die Wärmeversorgung, Energieerzeugung und Aspekte der Stadtplanung.\n\nIn solchen Sektorenübergreifenden Konzepten, die neben dem Klimaschutzkonzept existieren ist es wichtig, das Kimaschutz eine zentrale Rolle spielt.",
                verbose_name="Beziehen (sektorenübergreifende) Konzepte und Planungspapiere Klimaschutz mit ein?",
            ),
        ),
        migrations.AlterField(
            model_name="administrationchecklist",
            name="intersectoral_concepts_exists_rationale",
            field=models.TextField(
                blank=True,
                verbose_name="Begründung zu: Beziehen (sektorenübergreifende) Konzepte und Planungspapiere Klimaschutz mit ein?",
            ),
        ),
        migrations.AlterField(
            model_name="administrationchecklist",
            name="municipal_office_for_funding_management_exists",
            field=models.BooleanField(
                default=False,
                help_text="Beantragung für Fördermittel ist oft sehr zeitintensiv, und somit werden für Klimaschutz notwendige personelle Kapazitäten oft hierauf verwendet. Eigene Stellen sollen Entlastung schaffen und dafür sorgen, dass effizient an Klimaschutz gearbeitet werden kann.",
                verbose_name="Gibt es eine eigene kommunale Stelle für Fördermittelmanagement (unter anderem Beantragung etc. für den Klimaschutz)?",
            ),
        ),
        migrations.AlterField(
            model_name="administrationchecklist",
            name="municipal_office_for_funding_management_exists_rationale",
            field=models.TextField(
                blank=True,
                verbose_name="Begründung zu: Gibt es eine eigene kommunale Stelle für Fördermittelmanagement (unter anderem Beantragung etc. für den Klimaschutz)?",
            ),
        ),
        migrations.AlterField(
            model_name="capchecklist",
            name="sectors_of_climate_vision_used",
            field=models.BooleanField(
                default=False,
                help_text="Fast alle Kommunen führen ihre Treibhausgasbilanz mit BISKO (Bilanzierungs-Systematik Kommunal) durch. In dieser Systematik wird nur ein Teil der Industrie bilanziert, die Sektoren Abfall, Landwirtschaft und LULUCF fehlen völlig.\n\nDie Klimavision von LocalZero bilanziert die Sektoren Strom, Wärme, Verkehr, Industrie, Gebäude, Abfall, Landwirtschaft, LULUCF (Landnutzung, Landnutzungsänderungen und Forstwirtschaft).\n\nWenn die Kommune mit BISKO bilanziert ist es wichtig daraufhinzuweisen, dass die Bilanzierung ergänzt werden muss und vor allem in den fehlenden Sektoren trotzdem Maßnahmen entwickelt werden sollten.",
                verbose_name="Bilanziert der Klima-Aktionsplan vollständig, zum Beispiel in den Sektoren der Klimavision?",
            ),
        ),
        migrations.AlterField(
            model_name="capchecklist",
            name="sectors_of_climate_vision_used_rationale",
            field=models.TextField(
                blank=True,
                verbose_name="Begründung zu: Bilanziert der Klima-Aktionsplan vollständig, zum Beispiel in den Sektoren der Klimavision?",
            ),
        ),
        migrations.AlterField(
            model_name="capchecklist",
            name="target_date_exists",
            field=models.BooleanField(
                default=False,
                help_text="Die Jahreszahl (2035/20XX…) definiert, bis wann die Kommune – möglichst ohne Kompensation – klimaneutral werden will.\n\nDas bedeutet, dass allen Maßnahmen nachweisliche THG-Einsparmengen zugerechnet werden müssen, um dann als Ergebnis nachzuweisen, dass mit den geplanten Maßnahmen alle bilanzierten kommunalen THG-Emissionen eingespart werden.",
                verbose_name="Ist im Klima-Aktionsplan ein Zieljahr der Klimaneutralität hinterlegt?",
            ),
        ),
        migrations.AlterField(
            model_name="capchecklist",
            name="target_date_exists_rationale",
            field=models.TextField(
                blank=True,
                verbose_name="Begründung zu: Ist im Klima-Aktionsplan ein Zieljahr der Klimaneutralität hinterlegt",
            ),
        ),
        migrations.AlterField(
            model_name="capchecklist",
            name="tasks_have_responsible_entity",
            field=models.BooleanField(
                default=False,
                help_text="Ohne klar verteilte Verantwortlichkeiten können Maßnahmen nicht umgesetzt werden. Die Verantwortlichen können sowohl in der Kommunalverwaltung (z.B. Abteilungen) oder außerhalb (z.B. Stadtwerke) sein. Bei jeder vorgeschlagenen Maßnahme sollte die zuständige Fachabteilung, die kommunale Tochter oder sogar die zuständige Sachbearbeitung genannt werden.",
                verbose_name="Sind verantwortliche Personen/Fachbereiche/kommunale Gesellschaften für alle Maßnahmen hinterlegt?",
            ),
        ),
        migrations.AlterField(
            model_name="capchecklist",
            name="tasks_have_responsible_entity_rationale",
            field=models.TextField(
                blank=True,
                verbose_name="Begründung zu: Sind verantwortliche Personen/Fachbereiche/kommunale Gesellschaften für alle Maßnahmen hinterlegt?",
            ),
        ),
    ]
