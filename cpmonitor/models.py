from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from treebeard.mp_tree import MP_Node

# Note PEP-8 naming conventions for class names apply. So use the singular and CamelCase


class City(models.Model):
    class Meta:
        verbose_name = "Kommune"
        verbose_name_plural = "Kommunen"

    name = models.CharField("Name", max_length=255)
    zipcode = models.CharField("PLZ", max_length=5)
    url = models.URLField("Homepage", blank=True)

    introduction = models.TextField(
        "Einleitung",
        blank=True,
        help_text="""
            <p>Eine kurze Beschreibung der Situation in der Kommune.</p>
            <p>Kann in einer Übersicht aller Kommunen dargestellt werden.</p>
            <p>Deswegen möglichst kurz und ohne Formatierungen. Fett, Kursiv, Links, etc. sind okay.</p>
        """,
    )

    co2e_budget = models.IntegerField(
        "CO2e Budget [Mio Tonnen]",
        blank=True,
        default=0,
        help_text="Derzeit nicht genutzt.",
    )

    assessment_administration = models.TextField(
        "Bewertung Verwaltung",
        blank=True,
        help_text="""
            <p>Wie bewertet ihr die Nachhaltigkeitsarchitektur der Verwaltung?</p>
            <p>Die Checkliste hilft dabei, die Übersicht zu behalten.
            Es ist noch nicht klar, ob die Checkliste selber so angezeigt werden kann.
            Dieser Text sollte sie also zusammenfassen.</p>
            <p>Derzeit findest Du die Checkliste nur in der Master Struktur.</p>
        """,
    )

    # checklist_administration #72

    assessment_action_plan = models.TextField(
        "Bewertung Klimaaktionsplan",
        blank=True,
        help_text="""
            <p>Eine einleitende Übersicht in die Bewertung des Klimaaktionsplans der Kommune.</p>
            <p>Hier könnt Ihr zusammenfassen, was ihr als Ganzes von dem Plan haltet.</p>
            <p>Auf Sektorebene und bis zu den einzelnen Maßnahmen könnt Ihr weiter Details ergänzen.</p>""",
    )

    # checklist_action_plan #72

    assessment_status = models.TextField(
        "Bewertung Umsetzungsstand",
        blank=True,
        help_text="""
            <p>Eine einleitende Übersicht in die Bewertung des Umsetzungsstandes.</p>
            <p>Hält die Kommune sich im Wesentlichen an ihren eigenen Plan?</p>
            <p>Auf Sektorebene und bis zu den einzelnen Maßnahmen könnt Ihr weiter Details ergänzen.</p>""",
    )

    # images #58

    last_update = models.DateField("Letzte Aktualisierung", auto_now=True)

    contact_name = models.CharField(
        "Kontakt Name",
        max_length=255,
        blank=True,
        help_text="Name des Lokalteams oder einer Ansprechperson aus dem Lokalteam, das dieses Monitoring betreibt.",
    )
    contact_email = models.EmailField(
        "Kontakt E-Mail",
        blank=True,
        help_text="E-Mail Adresse, über die das Lokalteam erreicht werden kann.",
    )

    def __str__(self) -> str:
        return self.zipcode + " " + self.name


class Task(MP_Node):
    class Meta:
        verbose_name = "Sektor / Maßnahme"
        verbose_name_plural = "Sektoren und Maßnahmen"

    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        help_text="""
            <p>Bitte nicht ändern!</p>
            <p>Derzeit könnten dann die Strukturen der Klimaaktionspläne der Städte gehörig durcheinander geraten.</p>
            <p>Wir arbeiten noch an der Lösung, das zu verhindern.</p>
        """,
    )

    title = models.CharField(
        "Titel",
        max_length=255,
        help_text="""
            <p>Überschrift des Sektors, der Maßnahmengruppe oder der Maßnahme.</p>
            <p>Möglichst wie im Klimaaktionsplan angegeben.</p>
        """,
    )

    summary = models.TextField(
        "Kurztext",
        blank=True,
        help_text="""
            <p>Kann Beschreibung, Bewertung und Unsetzungsstand enthalten</p>
            <p>Kann in einer Übersicht meherer Sektoren / Maßnahmen dargestellt werden.</p>
            <p>Deswegen möglichst kurz und ohne Formatierungen. Fett, Kursiv, Links, etc. sind okay.</p>
        """,
    )

    # 1. Beschreibung: Inhalte aus dem KAP

    description = models.TextField(
        "Beschreibung",
        blank=True,
        help_text="""
            <p>Texte aus dem Klimaaktionsplan können hier eins-zu-eins eingegeben werden.</p>
            <p>Für Sektoren und Maßnahmengruppen sind Einleitungstexte aus dem Plan geeignet.</p>
            <p>Für Maßnahmen sollte hier die genaue Beschreibung stehen.</p>
        """,
    )

    planned_start = models.DateField(
        "Geplanter Start",
        blank=True,
        null=True,
        help_text="Nur falls im Klimaaktionsplan angegeben.",
    )

    planned_completion = models.DateField(
        "Geplantes Ende",
        blank=True,
        null=True,
        help_text="Nur falls im Klimaaktionsplan angegeben.",
    )

    responsible_organ = models.TextField(
        "Verantwortliches Organ",
        blank=True,
        help_text="""
            <p>Genauer Name des verantwortlichen Gremiums oder der verantwortlichen Behörde.</p>
            <p>Möglichst mit Ansprechperson, Kontaktdaten und was sonst notwendig ist, um Informationen einzuholen.</p>
            <p>Diese Informationen könnten später in separate Felder aufgeteilt werden.</p>
        """,
    )

    # 2. Bewertung der KAP Inhalte

    plan_assessment = models.TextField(
        "Bewertung der Planung",
        blank=True,
        help_text="""
            <p>Würde(n) die im Klimaaktionsplan beschriebenen Maßnahme(n) ausreichen, um das gesteckte Ziel zu erreichen?</p>
            <p>Sollte das gesteckte Ziel nicht ausreichen, kann das auch hier beschrieben werden.</p>
        """,
    )

    # 3. Umsetzungsstand

    class ExecutionAssessment(models.IntegerChoices):
        UNKNOWN = 0, "unbekannt (grau)"
        AHEAD = 1, "vor dem Plan (grün)"
        AS_PLANNED = 2, "im Plan (grün)"
        DELAYED = 3, "zurückgestellt / verzögert (orange)"
        INSUFFICIENT = 4, "nicht ausreichend / in Teilen gescheitert (rot)"
        FAILED = 5, "gescheitert (rot)"
        MISSING = 6, "fehlt im Plan (rot)"

    execution_assessment = models.IntegerField(
        "Bewertung des Umsetzungsstandes",
        choices=ExecutionAssessment.choices,
        default=ExecutionAssessment.UNKNOWN,
        help_text="""
            <p>Bei Maßnahmen: Wird/wurde die Maßnahme wie geplant umgesetzt?</p>
            <p>Bei Sektoren / Maßnahmengruppen:</p>
            <p>Wenn hier "unbekannt" ausgewählt wird, werden die Umsetzungsstände der Maßnahmen in diesem Sektor / dieser Gruppe zusammengefasst.</p>
            <p>Bei anderen Auswahlen wird diese Zusammenfassung überschrieben. Das sollte nur passieren, wenn sie unpassend oder irreführend ist.</p>
        """,
    )

    execution_justification = models.TextField(
        "Begründung der Bewertung",
        blank=True,
        help_text="Die Auswahl bei der Bewertung kann hier ausführlich begründet werden.",
    )

    class ExecutionProgress(models.IntegerChoices):
        UNKNOWN = 0, "unbekannt"
        NOT_PLANNED = 1, "ungeplant"
        PLANNED = 2, "in Zukunft geplant"
        IN_PROGRESS = 3, "läuft"
        FINISHED = 4, "abgeschlossen / gescheitert"

    execution_progress = models.IntegerField(
        "Fortschritt",
        choices=ExecutionProgress.choices,
        default=ExecutionProgress.PLANNED,
        help_text="""
            <p>Eine grobe Einteilung, wo sich diese Maßnahme zeitlich in der Planung befindet.</p>
            <p>Dies kann z.B. genutzt werden, um Maßnahmen zu filtern, deren Umsetzungsstand noch nicht bewertet werden kann.</p>
        """,
    )

    execution_completion = models.IntegerField(
        "Vervollständigungsgrad in Prozent",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="""
            <p>Bei wenigen Maßnahmen ist es möglich den Fortschritt quantitativ einzugeben. Nur bei solchen sollte hier ein Wert eingegeben werden.</p>
            <p>Ob und wie diese Zahlen angezeigt werden, ist noch unklar.</p>
        """,
    )

    actual_start = models.DateField(
        "Tatsächlicher Start",
        blank=True,
        null=True,
        help_text="Nur falls bekannt.",
    )

    actual_completion = models.DateField(
        "Tatsächlicher Ende",
        blank=True,
        null=True,
        help_text="Nur falls bekannt.",
    )

    def __str__(self) -> str:
        return self.title

    # Maybe later. Not part of the MVP:

    # class Severities(models.IntegerChoices):
    #     CRITICAL = 5
    #     HIGH = 4
    #     STANDARD = 3
    #     LOW = 2
    #     VERY_LOW = 1
    # severity = models.IntegerField(
    #     "Schweregrad",
    #     choices=Severities.choices,
    #     default=Severities.STANDARD)

    # weight = models.IntegerField(
    #     "Gewicht",
    #     default=0,
    #     validators=[
    #         MinValueValidator(0),
    #         MaxValueValidator(3)
    #     ]
    # )


# Tables for comparing and connecting the plans of all cities
# Lookup-entities (shared among all cities, entered by admins)

# This is currently kept out of the above city-specific data, since
# it might not be part of the MVP.

# Thoughts:
# - It might be better placed in a separate Django app, to keep it apart from the city stuff in the admin interface.
# - Sector / TaskCategory might be one table with recursive reference. Lets see, how that works out with the Tasks table.

# class Sector(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     ord = models.IntegerField(unique=True)

#     def __str__(self) -> str:
#         return self.name


# class TaskCategory(models.Model):
#     sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
#     name = models.CharField(max_length=200, unique=True)
#     info = models.TextField()
#     ord = models.IntegerField(unique=True)

#     def __str__(self) -> str:
#         return self.name


# class TaskToCategory(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.PROTECT)
#     category = models.ForeignKey(TaskCategory, on_delete=models.PROTECT)

#     def __str__(self) -> str:
#         return self.category.name + " - " + self.task.title
