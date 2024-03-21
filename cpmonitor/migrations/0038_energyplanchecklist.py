# Generated by Django 4.2.9 on 2024-03-18 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "cpmonitor",
            "0037_alter_administrationchecklist_intersectoral_concepts_exists_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="EnergyPlanChecklist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "energy_plan_exists",
                    models.BooleanField(
                        default=False,
                        verbose_name="Liegt ein öffentlich bekannt gemachter Beschluss zur Durchführung der Wärmeplanung vor?",
                    ),
                ),
                (
                    "energy_plan_exists_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "schedule_exists",
                    models.BooleanField(
                        default=False,
                        verbose_name="Enthält der Beschluss einen Zeitplan für die Durchführung der Wärmeplanung (Ausschreibung, Beauftragung, Durchführung)?",
                    ),
                ),
                (
                    "schedule_exists_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "hydrogen_grid_examined",
                    models.BooleanField(
                        default=False,
                        verbose_name="Wurde ein frühzeitiger Ausschluss von Wasserstoffnetzen geprüft und das Ergebnis der Prüfung begründet?",
                    ),
                ),
                (
                    "hydrogen_grid_examined_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "thermal_grid_examined",
                    models.BooleanField(
                        default=False,
                        verbose_name="Wurde ein frühzeitiger Ausschluss von Wärmenetzen geprüft und das Ergebnis der Prüfung begründet?",
                    ),
                ),
                (
                    "thermal_grid_examined_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "demand_specified",
                    models.BooleanField(
                        default=False,
                        verbose_name="Ergibt sich ein klares gebäudescharfes Bild des Wärmebedarfs und der aktuellen Wärmeversorgungsart?",
                    ),
                ),
                (
                    "demand_specified_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "demand_specified_on_a_map",
                    models.BooleanField(
                        default=False,
                        verbose_name="Sind die Wärmebedarfe und -versorgungsarten räumlich auf Karten aufgelöst dargestellt (inkl. Netzinfrastrukturen + Wärmedichten in jeder Straße)?",
                    ),
                ),
                (
                    "demand_specified_on_a_map_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "potential_determined",
                    models.BooleanField(
                        default=False,
                        verbose_name="Wurden alle sinnvollen Potenziale zur erneuerbaren Wärmeerzeugung und -speicherung erfasst?",
                    ),
                ),
                (
                    "potential_determined_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "demand_reduction_planned",
                    models.BooleanField(
                        default=False,
                        verbose_name="Sind kommunale Maßnahmen zur Senkung des Wärmebedarfs enthalten (siehe sektorübergreifende Maßnahmen)?",
                    ),
                ),
                (
                    "demand_reduction_planned_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "paris_agreement_compliant",
                    models.BooleanField(
                        default=False,
                        verbose_name="Folgt das Zielszenario Paris-konformen Zielsetzungen und Grundsätzen der kommunalen Wärmeplanung?",
                    ),
                ),
                (
                    "paris_agreement_compliant_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "is_efficient",
                    models.BooleanField(
                        default=False,
                        verbose_name="Werden die möglichst effizienten und erneuerbaren Wärmequellen erschlossen?",
                    ),
                ),
                (
                    "is_efficient_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "has_intermediate_goals",
                    models.BooleanField(
                        default=False,
                        verbose_name="Sind Zwischenziele für die Erreichung des Zielszenarios enthalten?",
                    ),
                ),
                (
                    "has_intermediate_goals_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "effect_on_electricity_demand",
                    models.BooleanField(
                        default=False,
                        verbose_name="Wie verändert sich der Strombedarf durch den veränderten Wärmebedarf? Werden kommunale Maßnahmen getroffen, um den größeren Strombedarf regional bereitzustellen?",
                    ),
                ),
                (
                    "effect_on_electricity_demand_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "designation_of_areas",
                    models.BooleanField(
                        default=False,
                        verbose_name="Gibt es eine zeitlich nachvollziehbare Planung für die Ausweisung der Gebiete, d.h. ab wann, welche Gebiete mit welcher Versorgung ausgebaut werden sollen?",
                    ),
                ),
                (
                    "designation_of_areas_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "criteria_comprehensible",
                    models.BooleanField(
                        default=False,
                        verbose_name="Wird dies erklärt bzw. wird deutlich, warum bzw. basierend auf welchen Kriterien (Topographie, Wärmebedarfsdichte, zentrale erneuerbare Wärmequellen etc.)?",
                    ),
                ),
                (
                    "criteria_comprehensible_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "based_on_analyses",
                    models.BooleanField(
                        default=False,
                        verbose_name="Ergibt sich die Einteilung in voraussichtliche Wärmeversorgungsgebiete aufgrund der vorherigen Analysen?",
                    ),
                ),
                (
                    "based_on_analyses_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "effective_measures",
                    models.BooleanField(
                        default=False,
                        verbose_name="Entwickelt die Kommune (bzw. die von ihr beauftragten Akteure) einen aus den Potenzialen und Zielszenario abgeleiteten ambitionierten Transformationspfad mit effektiven Maßnahmen?",
                    ),
                ),
                (
                    "effective_measures_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "energy_sources_sustainable",
                    models.BooleanField(
                        default=False,
                        verbose_name="Basieren die darauffolgend entwickelten Transformationspläne auf den von LocalZero empfohlenen Wärmequellen (und z.B. nicht wesentlich auf Wasserstoff oder Biomasse)?",
                    ),
                ),
                (
                    "energy_sources_sustainable_rationale",
                    models.TextField(blank=True, verbose_name="Begründung"),
                ),
                (
                    "city",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="energy_plan_checklist",
                        to="cpmonitor.city",
                    ),
                ),
            ],
            options={
                "verbose_name": "Wärmeplanung Checkliste",
            },
        ),
    ]
