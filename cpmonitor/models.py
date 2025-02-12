from datetime import date
from django.conf import settings
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.http import HttpRequest
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils import timezone
from invitations.app_settings import app_settings as invitations_app_settings
from invitations.base_invitation import AbstractBaseInvitation
from invitations import signals
from treebeard.exceptions import InvalidPosition
from treebeard.mp_tree import MP_Node
from types import NoneType

from PIL import Image


# Note PEP-8 naming conventions for class names apply. So use the singular and CamelCase


class City(models.Model):
    """Base data for a city or municipality.

    Some background for the handling of the `slug` field:
    The slug is used in all URLs for the city. Therefore it has to be unique.
    Usually, e.g. in a blog system, slugs are never updated.
    Here it is updated, since it is quite important to have an URL with the slug based on the current name.
    When the slug is updated, the uniqueness has to be checked again.
    However, when `editable=False` is set, django admin prevents that.
    See clean() and vallidate_unique() for technical details.
    """

    class Meta:
        verbose_name = "Kommune"
        verbose_name_plural = "Kommunen"

    draft_mode = models.BooleanField(
        "Entwurfs-Modus",
        default=True,
        help_text=(
            "Im Entwurfs-Modus ist die Kommune für normale Besucher im Frontend unsichtbar."
            " Nur wenn im gleichen Browser ein User im Admin angemeldet ist, wird sie angezeigt."
        ),
    )

    name = models.CharField(
        "Name",
        max_length=50,
        help_text="""
            <p>Name der Kommune. Maximal 50 Zeichen.</p>
        """,
    )
    zipcode = models.CharField("PLZ", max_length=5)
    municipality_key = models.CharField(
        "Gemeindeschlüssel", max_length=8, blank=True, null=True
    )
    url = models.URLField("Homepage", blank=True)

    city_editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="Kommunen-Bearbeiter",
        related_name="edited_cities",
        help_text="""
            <p>Diese Benutzer können alle Inhalte der Kommune bearbeiten.</p>
        """,
    )

    city_admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="Kommunen-Admins",
        related_name="administered_cities",
        help_text="""
            <p>Diese Benutzer können zusätzlich andere Benutzter als Admins und Bearbeiter eintragen.</p>
            <p>Sie brauchen nicht als "Bearbeiter" eingetragen zu werden.</p>
        """,
    )

    resolution_date = models.DateField(
        "Datum des Klimaneutralitäts-Beschlusses",
        blank=True,
        null=True,
    )

    target_year = models.IntegerField(
        "Zieljahr Klimaneutralität", blank=True, null=True, help_text="z.B. 2035"
    )

    show_roof_pv_indicator = models.BooleanField(
        "Graphik Entwicklung Dach-PV",
        default=False,
        help_text="""
            Graphik zur Entwicklung der Dach-PV anzeigen. Daten werden automatisch aus dem
            Marktstammdatenregister bezogen. Der Gemeindeschlüssel muss dazu ausgefüllt sein.
        """,
    )

    teaser = models.CharField(
        "Teaser",
        max_length=200,
        blank=True,
        help_text="""
            <p>Eine kurze Beschreibung der Situation in der Kommune. Maximal 200 Zeichen. Keine Formatierungen.</p>
            <p>Kann in einer Übersicht aller Kommunen oder als Vorschau eines Links dargestellt werden.</p>
        """,
    )

    description = models.TextField(
        "Beschreibung",
        blank=True,
        help_text="""
            <p>Ein einleitender Text, der die wesentlichen Inhalte zusammenfasst und/oder einen Überblick über die weiteren Inhalte gibt.</p>
            <p>Dieser wird nur auf der Seite der Kommune angezeigt unter einem fett gedruckten Absatz, der den Teaser enthält.</p>
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

    assessment_action_plan = models.TextField(
        "Bewertung Klimaaktionsplan",
        blank=True,
        help_text="""
            <p>Eine einleitende Übersicht in die Bewertung des Klimaaktionsplans der Kommune.</p>
            <p>Hier könnt Ihr zusammenfassen, was ihr als Ganzes von dem Plan haltet.</p>
            <p>Auf Ebene der Handlungsfelder und bei den einzelnen Maßnahmen könnt Ihr weiter Details ergänzen.</p>""",
    )

    assessment_status = models.TextField(
        "Bewertung Umsetzungsstand",
        blank=True,
        help_text="""
            <p>Eine einleitende Übersicht in die Bewertung des Umsetzungsstandes.</p>
            <p>Hält die Kommune sich im Wesentlichen an ihren eigenen Plan?</p>
            <p>Auf Ebene der Handlungsfelder und bei den einzelnen Maßnahmen könnt Ihr weiter Details ergänzen.</p>""",
    )

    last_update = models.DateField("Letzte Aktualisierung", auto_now=True)

    contact_name = models.CharField(
        "Kontakt Name",
        max_length=255,
        blank=True,
        help_text=(
            "Name des Lokalteams oder einer Ansprechperson aus dem Lokalteam, das dieses Monitoring"
            " betreibt."
        ),
    )
    contact_email = models.EmailField(
        "Kontakt E-Mail",
        blank=True,
        help_text="E-Mail Adresse, über die das Lokalteam erreicht werden kann.",
    )

    internal_information = models.TextField(
        "Interne Informationen",
        blank=True,
        help_text="""
            <p>Interne Informationen, Notizen, Referenzen etc.</p>
            <p>Die hier angegebenen Informationen werden nur in der Admin-Oberfläche angezeigt und nicht im Frontend.</p>
        """,
    )

    supporting_ngos = models.TextField(
        "Unterstützung von",
        blank=True,
        help_text="hier kann die Unterstüzung von anderen NGOs gewürdigt werden",
    )

    def __str__(self) -> str:
        return self.zipcode + " " + self.name

    slug = models.SlugField(
        "slug",
        max_length=255,
        unique=True,
        editable=False,
    )

    def clean(self):
        """Set / update the slug on every validation. (Done by admin before `save()`)"""
        self.slug = slugify(self.name)

    def validate_unique(self, exclude=None):
        """
        Add slug to fields to validate uniqueness and convert a slug error to non-field error.

        This is necessary, because `editable=False` excludes the field from validation
        and cannot handle field-based validation errors.
        """
        exclude.remove("slug")
        try:
            super().validate_unique(exclude=exclude)
        except ValidationError as e:
            msgs = e.message_dict
            slug_errors = msgs.pop("slug", None)
            if slug_errors:
                slug_errors.append(
                    "Der Name der Kommune wird in der URL als '%(slug)s' geschrieben. Das"
                    " kollidiert mit einer anderen Stadt." % {"slug": self.slug}
                )
                if not NON_FIELD_ERRORS in msgs:
                    msgs[NON_FIELD_ERRORS] = []
                msgs[NON_FIELD_ERRORS].extend(slug_errors)
            raise ValidationError(msgs)

    def save(self, *args, **kwargs):
        "Ensure there are all needed invitation links for the city."
        super().save(*args, **kwargs)
        Invitation.ensure_for_city(self)


class CapChecklist(models.Model):
    class Meta:
        verbose_name = "Checkliste zum KAP"
        verbose_name_plural = "Checklisten zum KAP"

    def __str__(self):
        return "Checkliste zum KAP für " + self.city.name

    city = models.OneToOneField(
        City,
        on_delete=models.PROTECT,
        related_name="cap_checklist",
        verbose_name="Stadt",
    )

    cap_exists = models.BooleanField(
        "Gibt es einen Klima-Aktionsplan?",
        default=False,
        help_text="Ein Klima-Aktionsplan (auch KAP / Klimaschutzkonzept / integriertes Klimaschutzkonzept) ist ein von "
        "einer Kommune beschlossener Plan/Konzept, in dem beispielhaft oder auch in mehreren Szenarien "
        "festgelegt ist, wie die Kommune bis 2035/20XX klimaneutral wird.\n\n"
        "Im ersten Teil des KAPs wird bilanziert: Wieviel Treibhausgase emittiert die Kommune derzeit?\n\n"
        "Im zweiten Teil des KAPs werden Maßnahmen aufgelistet, mit denen die Kommune klimaneutral werden "
        "kann. Dabei ist nicht nur Emissionsreduktion sondern die Erreichung der Klimaneutralität in allen "
        "Bereichen der Kommune von Bedeutung.",
    )
    cap_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    target_date_exists = models.BooleanField(
        "Ist im Klima-Aktionsplan ein Zieljahr der Klimaneutralität hinterlegt?",
        default=False,
        help_text="Die Jahreszahl (2035/20XX…) definiert, bis wann die Kommune – möglichst ohne Kompensation – "
        "klimaneutral werden will.\n\n"
        "Das bedeutet, dass allen Maßnahmen nachweisliche THG-Einsparmengen zugerechnet werden müssen, um dann als "
        "Ergebnis nachzuweisen, dass mit den geplanten Maßnahmen alle bilanzierten kommunalen THG-Emissionen "
        "eingespart werden.",
    )
    target_date_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    based_on_remaining_co2_budget = models.BooleanField(
        "Sind die Einsparziele im Klima-Aktionsplan auf Grundlage des Restbudgets berechnet?",
        default=False,
        help_text="Das Restbudget beschreibt das globale Kontingent an Treibhausgasen (THG), das für die Einhaltung "
        "des Pariser Klimaabkommens zukünftig noch emittiert werden kann. Dieses THG-Kontingent kann auf "
        "einzelne Nationen und wiederum auf Kommunen heruntergebrochen werden. Jede Kommune hat somit ein "
        "„persönliches kommunales Restbudget“, das sie für die Einhaltung des Pariser 1,5 Grad Zieles nicht "
        "überschreiten darf.",
    )
    based_on_remaining_co2_budget_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    sectors_of_climate_vision_used = models.BooleanField(
        "Bilanziert der Klima-Aktionsplan vollständig, zum Beispiel in den Sektoren der Klimavision?",
        default=False,
        help_text="Fast alle Kommunen führen ihre Treibhausgasbilanz mit BISKO (Bilanzierungs-Systematik Kommunal) "
        "durch. In dieser Systematik wird nur ein Teil der Industrie bilanziert, die Sektoren Abfall, "
        "Landwirtschaft und LULUCF fehlen völlig.\n\n"
        "Die Klimavision von LocalZero bilanziert die Sektoren Strom, Wärme, Verkehr, Industrie, Gebäude, "
        "Abfall, Landwirtschaft, LULUCF (Landnutzung, Landnutzungsänderungen und Forstwirtschaft).\n\n"
        "Wenn die Kommune mit BISKO bilanziert ist es wichtig daraufhinzuweisen, dass die Bilanzierung ergänzt werden "
        "muss und vor allem in den fehlenden Sektoren trotzdem Maßnahmen entwickelt werden sollten.",
    )
    sectors_of_climate_vision_used_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    scenario_for_climate_neutrality_till_2035_exists = models.BooleanField(
        "Enthält der Klima-Aktionsplan ein Szenario mit dem Ziel Klimaneutralität bis 2035?",
        default=False,
        help_text="Das Szenario soll zeigen wie die Kommune unter realistischen Bedinungen (politischer Entwicklung, "
        "Dauer der Maßnahmen etc.) ihre Emissionen auf Netto-Null reduzieren kann, oder wie weit eine "
        "Reduktion realistisch aber ambitioniert möglich ist.\n\n"
        "Oft ist im KAP ein weiteres Szenario mit einem anderen Zieljahr hinterlegt zum Bsp. 2040 oder 2045",
    )
    scenario_for_climate_neutrality_till_2035_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    scenario_for_business_as_usual_exists = models.BooleanField(
        "Ist ein Trendszenario hinterlegt?",
        default=False,
        help_text="Ein Trendszenario zeigt auf, wie sich die kommunalen Emissionen entwickeln, wenn die Kommune keine "
        "Maßnahmen in Richtung Klimaneutralität ergreift, also „business as usual“ betreibt. In diesem "
        "Fall können sich die kommunalen Emissionen trotzdem verändern, da bundespolitische Maßnahmen "
        "Einfluss auf kommunale Emissionen haben (Bsp: veränderter Bundesdeutscher Strommix).",
    )
    scenario_for_business_as_usual_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    annual_costs_are_specified = models.BooleanField(
        "Sind die jährlichen Kosten und der jährliche Personalbedarf der Maßnahmen ausgewiesen?",
        default=False,
        help_text="Die jährlichen Kosten für Maßnahmen, sowie Kosten für den Personalbedarf für die Umsetzung der "
        "Maßnahmen, machen den Aufwand einschätzbar und liefern Sicherheit für die Planung der Umsetzung.\n\n"
        "Sind keine Kosten und keine Personalstellen hinterlegt sinkt die Wahrscheinlichkeit, dass die "
        "Politik diese Maßnahme schnell freigibt. Denn die Kosten und der nötige Personalumfang muss erst "
        "ermittelt werden.",
    )
    annual_costs_are_specified_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    tasks_are_planned_yearly = models.BooleanField(
        "Haben die Maßnahmen eine jahresscharfe Planung?",
        default=False,
        help_text="Eine genaue Planung der Maßnahmen ist eine Grundvoraussetzung, um den Erfolg/Fortschritt der "
        "Umsetzung des Klima-Aktionsplans zu messen. Optimal ist ein Ablaufplan, in dem die Reihenfolge und "
        "die zeitliche Überschneidung aller Maßnahmen genau aufgeschlüsselt ist.\n\n"
        "Mit einem solchen Ablaufplan kann die Kommune die Reduktion der THG-Emissionen für jedes kommende Jahr "
        "prognostizieren und so nachweisen, dass sie das 1,5 Grad Ziel einhält.\n\n"
        "Wichtig ist natürlich, dass zuerst die großen Emittenden auf Klimaneutralität umgestellt werden und danach bei "
        "den kleinen Emissionsquellen Maßnahmen ergriffen werden.",
    )
    tasks_are_planned_yearly_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    tasks_have_responsible_entity = models.BooleanField(
        "Sind verantwortliche Personen/Fachbereiche/kommunale Gesellschaften für alle Maßnahmen hinterlegt?",
        default=False,
        help_text="Ohne klar verteilte Verantwortlichkeiten können Maßnahmen nicht umgesetzt werden. Die "
        "Verantwortlichen können sowohl in der Kommunalverwaltung (z.B. Abteilungen) oder außerhalb (z.B. "
        "Stadtwerke) sein. Bei jeder vorgeschlagenen Maßnahme sollte die zuständige Fachabteilung, "
        "die kommunale Tochter oder sogar die zuständige Sachbearbeitung genannt werden.",
    )
    tasks_have_responsible_entity_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    annual_reduction_of_emissions_can_be_predicted = models.BooleanField(
        "Wird anhand der Maßnahmen ein jährlicher Reduktionspfad des Energiebedarfs und der THG-Emissionen ersichtlich?",
        default=False,
        help_text="Aus dem genauen Zeitplan der Maßnahmenplanung kann ab jetzt bis zum Jahr der Klimaneutralität ("
        "2035/20XX) die THG-Emissionen und der Endenergiebedarf jährlich prognostiziert werden in allen "
        "Sektoren. Wird z.B. ein Braunkohlewerk im Jahr X geschlossen, sinken die Emissionen um Y. Dadurch "
        "wird der Weg zur Treibhausgasneutralität klar erkennbar und zu kompensierende Emissionen sichtbar.",
    )
    annual_reduction_of_emissions_can_be_predicted_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    concept_for_participation_specified = models.BooleanField(
        "Gibt es ein gutes Konzept zur Akteur:innenbeteiligung?",
        default=False,
        help_text="Alle Akteur:innen in einer Kommune sollten bei der Erstellung/Umsetzung eines KAPs beteiligt "
        "werden. Unterschiedliche Akteur:innen der Kommune sind: Bürger:innen (z.B. LocalZero-Teams), "
        "Verwaltung der Kommune, höchste politische Gremien der Kommune, Stakeholder:innen in der Kommune ("
        "z.B. kommunale Unternehmen oder Vereine).",
    )
    concept_for_participation_specified_rationale = models.TextField(
        "Begründung",
        blank=True,
    )


class AdministrationChecklist(models.Model):
    class Meta:
        verbose_name = "Checkliste zu Verwaltungsstrukturen"
        verbose_name_plural = "Checklisten zu Verwaltungsstrukturen"

    def __str__(self):
        return "Checkliste zu Verwaltungsstrukturen für " + self.city.name

    city = models.OneToOneField(
        City,
        on_delete=models.PROTECT,
        related_name="administration_checklist",
        verbose_name="Stadt",
    )

    climate_protection_management_exists = models.BooleanField(
        "Gibt es ein Klimaschutzmanagement, das befugt ist, Entscheidungen zu treffen und über Haushaltsmittel verfügt?",
        default=False,
        help_text="Klimaschutzmanager:innen können von der Nationalen Initiative für Klimaschutz (NKI) gefördert "
        "werden. Allerdings ist wichtig, dass das Klimaschutzmanagement an einer Stelle in der Verwaltung "
        "angesiedelt ist, wo es Entscheidungen treffen und möglichst frei agieren kann sowie über "
        "finanzielle Mittel verfügt. Im Besten Falle ist das Klimaschutzmanagement als Stabsstelle "
        "organisiert, die Klimaschutzmanagerin ist also keine Sachbearbeiterin, die einer Fachdienstleitung "
        "unterstellt ist, sondern selber ein Fachdienst.",
    )
    climate_protection_management_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    climate_relevance_check_exists = models.BooleanField(
        "Klimarelevanzprüfung: werden alle Beschlüsse von Verwaltung und Politik auf die Auswirkungen auf das Klima geprüft?",
        default=False,
        help_text="Klimaschutz ist wichtig und muss als Querschnittsaufgabe umgesetzt werden. Alle "
        "Sachbearbeiterinnen, die Leitungsebene und auch die Politik muss – um Klimaneutralität zu erreichen "
        "– in allen Planungen Klimaschutz berücksichtigen!\n\n"
        "Daher ist es wesentlich, alle kommunalen Beschlüsse hinsichtlich ihrer Verträglichkeit mit Klimaschutz zu "
        "bewerten. Dies erfolgt durch eine Integration eines „Klima-Checks“/Klimarelevanzprüfung/"
        "Klimaschutzrelevanzprüfung in alle Beschlussvorlagen. Gesetzlich geregelt ist bisher nur, "
        "dass alle Beschlüsse auf ihre finanziellen Auswirkungen hin geprüft werden müssen. Unter jedem "
        "kommunalen Beschluss steht also ein kurzer Absatz über die Höhe der Kosten und eine Information,"
        "ob dies wiederkehrende Kosten sind.\n\n"
        "Hier würden mit der Einführung einer Klimarelevanzprüfung weitere Informationen angefügt: Hat der Beschluss negative oder positive Auswirkungen auf den Klimaschutz, wurden Alternativen geprüft, warum wurden diese verworfen etc.\n\n"
        "Beschlüsse werden somit bereits während der Erstellung durch die Sachbearbeiter:innen in den Fachbereichen auf ihre Klimarelevanz hin (vor-)bewertet und Aspekte des Klimaschutzes sind automatisch integraler Bestandteil jeder Beschlussfassung. Klimafolgen werden somit transparent, Politiker:innen können fundierter entscheiden. Langfristig baut die Kommune Kompetenzen auf, um die Auswirkung auf das Klima bei allen relevanten Entscheidungen zu berücksichtigen.",
    )
    climate_relevance_check_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    climate_protection_monitoring_exists = models.BooleanField(
        "Gibt es ein Monitoring von Kimaschutzmaßnahmen?",
        default=False,
        help_text="Monitoring bedeutet ein Überwachen/Überblick über den Erfolg von Klimaschutzmaßnahmen. In einem "
        "kommunalen Monitoring sollten die eingesparten Emissionen sichtbar gemacht werden und mit den "
        "Prognosen aus dem Klimaschutzkonzept verglichen werden. Falls die Kommune nicht im Zeitplan liegt: "
        "Wie soll nachgesteuert werden?\n\n"
        "Das Monitoring ist wichtig, um das Ziel der Klimaneutralität und notwendige Schritte im Auge zu "
        "behalten.",
    )
    climate_protection_monitoring_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    intersectoral_concepts_exists = models.BooleanField(
        "Beziehen (sektorenübergreifende) Konzepte und Planungspapiere Klimaschutz mit ein?",
        default=False,
        help_text="Sektorenübergreifende Konzepte sind zum Beispiel Kimaanpassungs- , Konzepte der Städtebauförderung "
        "oder Quartierskonzepte. Diese Konzepte betrachten Maßnahmen, die über mehrere Sektoren gehen, "
        "das Quartierskonzept betrachtet zum Beispiel die Gebäudesanierung, die Wärmeversorgung, "
        "Energieerzeugung und Aspekte der Stadtplanung.\n\n"
        "In solchen Sektorenübergreifenden Konzepten, die neben dem Klimaschutzkonzept existieren ist es wichtig, "
        "das Kimaschutz eine zentrale Rolle spielt.",
    )
    intersectoral_concepts_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    guidelines_for_sustainable_procurement_exists = models.BooleanField(
        "Gibt es Richtlinien für ein nachhaltiges Beschaffungswesen?",
        default=False,
        help_text="Die Kommunalverwaltung kann aufgrund ihres großen Beschaffungsvolumens mit ihrer Nachfrage "
        "energieeffiziente Produkte fördern und damit einen wichtigen Beitrag zum Klimaschutz leisten. "
        "Wichtig ist, möglichst nur Produkte und Dienstleistungen zu erwerben, die wirklich benötigt werden "
        "und im Sinne der Nachhaltigkeit neben einer hohen Umweltverträglichkeit auch sozialen wie "
        "ökonomischen Aspekten entsprechen. Umweltfreundliche Beschaffung sollte in grundlegenden "
        "Dokumenten der Behörde wie dem eigenen Leitbild, verpflichtenden Dienstanweisungen oder einem "
        "Beschaffungsleitfaden als Organisationsziel definiert werden.",
    )
    guidelines_for_sustainable_procurement_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    municipal_office_for_funding_management_exists = models.BooleanField(
        "Gibt es eine eigene kommunale Stelle für Fördermittelmanagement (unter anderem Beantragung etc. für den Klimaschutz)?",
        default=False,
        help_text="Beantragung für Fördermittel ist oft sehr zeitintensiv, und somit werden für Klimaschutz "
        "notwendige personelle Kapazitäten oft hierauf verwendet. Eigene Stellen sollen Entlastung schaffen "
        "und dafür sorgen, dass effizient an Klimaschutz gearbeitet werden kann.",
    )
    municipal_office_for_funding_management_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    public_relation_with_local_actors_exists = models.BooleanField(
        "Gibt es einen Klimabeirat/Klimarat/Bürger:innenrat? Ist so ein Gremium in der Kommune eingerichtet und tagt regelmäßig?",
        default=False,
        help_text="Mit Klimabeirat/Klimarat/Bürger:innenrat sind Gremien gemeint, die ausBürgerperspektive die "
        "Lokalpolitik beraten. Um politischen Einfluss auszuüben sollten diese regelmäßig tagen.",
    )
    public_relation_with_local_actors_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )


class EnergyPlanChecklist(models.Model):
    class Meta:
        verbose_name = "Checkliste zur Wärmeplanung"
        verbose_name_plural = "Checklisten zur Wärmeplanung"

    def __str__(self):
        return "Checkliste zur Wärmeplanung für " + self.city.name

    city = models.OneToOneField(
        City,
        on_delete=models.PROTECT,
        related_name="energy_plan_checklist",
        verbose_name="Stadt",
    )

    energy_plan_exists = models.BooleanField(
        "Liegt ein öffentlich bekannt gemachter Beschluss zur Durchführung der Wärmeplanung vor?",
        default=False,
    )
    energy_plan_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    schedule_exists = models.BooleanField(
        "Enthält der Beschluss einen Zeitplan für die Durchführung der Wärmeplanung (Ausschreibung, Beauftragung, Durchführung)?",
        default=False,
    )
    schedule_exists_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    hydrogen_grid_examined = models.BooleanField(
        "Wurde ein frühzeitiger Ausschluss von Wasserstoffnetzen geprüft und das Ergebnis der Prüfung begründet?",
        default=False,
        help_text="Ein potenzielles Wasserstoffgebiet kann hier bereits ausgeschlossen werden, wenn eine Eignung als sehr unwahrscheinlich eingestuft wird. Das ist zu dem Zeitpunkt der Wärmeplanung dann möglich, wenn entweder kein Gasnetz besteht oder bereits absehbar ist, dass eine künftige Versorgung mit Wasserstoff nicht wirtschaftlich sein wird. Disclaimer: Wasserstoffnetze sollten grundsätzlich ausgeschlossen werden: Verfügbarkeit und Kosten unsicher. Mit welcher Begründung geschieht dies vor Ort nicht?",
    )
    hydrogen_grid_examined_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    thermal_grid_examined = models.BooleanField(
        "Wurde ein frühzeitiger Ausschluss von Wärmenetzen geprüft und das Ergebnis der Prüfung begründet?",
        default=False,
        help_text="Ein potenzielles Wärmenetz kann hier bereits ausgeschlossen werden, wenn es entweder kein Wärmenetz gibt oder die Siedlungsstruktur (niedrige Wärmebedarfsdichte / hohe Zersiedelung) es nicht sinnvoll erscheinen lässt. Wenn Wärmenetze objektiv schlechte Lösungen sind, sollten sie frühzeitig ausgeschlossen werden um Planungskosten zu sparen und hohe Heizkosten am Ende des Tages zu vermeiden. Mit welcher Begründung geschieht dies vor Ort nicht?",
    )
    thermal_grid_examined_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    demand_specified = models.BooleanField(
        "Ergibt sich ein klares gebäudescharfes Bild des Wärmebedarfs und der aktuellen Wärmeversorgungsart?",
        default=False,
        help_text=mark_safe(
            'Sind alle oder zumindest die wichtigsten Bilanzen  und Kennzahlen der Gemeinde vorhanden?<br/>Wichtige Bilanzen:<ul><li>Energiebilanz</li><li>Treibhausgasbilanzen</li><li>räumlich aufgelöster Wärmebedarf</li></ul>Mögliche Kenngrößen:<ul><li>Wohnflächen</li><li>Nutzungsarten der Gebäude</li><li>Flächendichten</li><li>Gebäudetypen und Baualtersklassen</li><li>Versorgungs- und Beheizungsstruktur der Gebäude</li></ul><a target="_blank" href="https://www.kea-bw.de/waermewende/wissensportal/leistungsverzeichnis-kwp">Mehr Infos hier</a> (Leistungsverzeichnis A.1.1).'
        ),
    )
    demand_specified_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    demand_specified_on_a_map = models.BooleanField(
        "Sind die Wärmebedarfe und -versorgungsarten räumlich auf Karten aufgelöst dargestellt (inkl. Netzinfrastrukturen + Wärmedichten in jeder Straße)?",
        default=False,
    )
    demand_specified_on_a_map_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    potential_determined = models.BooleanField(
        "Wurden alle sinnvollen Potenziale zur erneuerbaren Wärmeerzeugung und -speicherung erfasst?",
        default=False,
        help_text=mark_safe(
            'Es ist wichtig, dass sowohl umfangreich als auch priorisiert Wärmequellen berücksichtigt werden. <a target="_blank" href="https://mitmachen-wiki.germanzero.org/w/LocalZero:Empfohlene_Erschlie%C3%9Fung_folgender_erneuerbarer_W%C3%A4rmequellen_und_%E2%80%93_speicher">LocalZero Liste der empfohlenen Wärmequellen.</a>'
        ),
    )
    potential_determined_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    demand_reduction_planned = models.BooleanField(
        "Sind kommunale Maßnahmen zur Senkung des Wärmebedarfs enthalten (siehe sektorübergreifende Maßnahmen)?",
        default=False,
        help_text=mark_safe(
            '<a target="blank" href="https://mitmachen-wiki.germanzero.org/w/LocalZero:Integration_betroffener_Sektoren">LocalZero Liste der betroffenen Sektoren</a>'
        ),
    )
    demand_reduction_planned_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    communication_potential = models.BooleanField(
        "Werden die Ergebnisse der Potenzialanalyse inkl. der Möglichkeit zur Kommentierung zugänglich gemacht? Gibt es eine Möglichkeit die Ergebnisse mit der Kommune zu diskutieren?",
        default=False,
        help_text=mark_safe(
            "Die Potenzialanalyse sollte inkl. der geplanten Maßnahmen öffentlich vorgestellt werden und zur Kommentierung offengelegt werden. Hier muss die Möglichkeit Feedback zu geben geschaffen werden, um ggf. die Potenzialanalyse noch anzupassen. Das ist wichtig, denn basierend auf der Potenzialanalyse wird das Zielszenario entwickelt.<br/>Gesetzlich vorgeschrieben ist lediglich die einmalige digitale Einsicht in die Pläne nach Erstellung des Entwurfs des Zielszenarios und der Einteilung in voraussichtliche Wärmeversorgunsgebiete inkl. Umsetzungsstrategie (§ 20 WPG, s.u.) für die Dauer von 30 Tagen zur Abgabe von Stellungnahmen."
        ),
    )
    communication_potential_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    paris_agreement_compliant = models.BooleanField(
        "Folgt das Zielszenario Paris-konformen Zielsetzungen und Grundsätzen der kommunalen Wärmeplanung?",
        default=False,
        help_text=mark_safe(
            "Damit wir in Deutschland dem Pariser Klimaabkommen entsprechen, müssen wir im Restbudget bleiben. Das bedeutet für jede Kommune:<ul><li>Wird ein möglichst 100% Anteil lokaler Erneuerbarer Energien zur Wärmeerzeugung erreicht?</li><li>Bis 2035?</li><li>Mit den von LocalZero empfohlenen Wärmeanwendungen?</li></ul>"
        ),
    )
    paris_agreement_compliant_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    is_efficient = models.BooleanField(
        "Werden die möglichst effizienten und erneuerbaren Wärmequellen erschlossen?",
        default=False,
        help_text=mark_safe(
            '<a target="_blank" href="https://mitmachen-wiki.germanzero.org/w/LocalZero:Empfohlene_Erschlie%C3%9Fung_folgender_erneuerbarer_W%C3%A4rmequellen_und_%E2%80%93_speicher">LocalZero Liste der Wärmequellen</a>'
        ),
    )
    is_efficient_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    has_intermediate_goals = models.BooleanField(
        "Sind Zwischenziele für die Erreichung des Zielszenarios enthalten?",
        default=False,
    )
    has_intermediate_goals_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    effect_on_electricity_demand = models.BooleanField(
        "Wie verändert sich der Strombedarf durch den veränderten Wärmebedarf? Werden kommunale Maßnahmen getroffen, um den größeren Strombedarf regional bereitzustellen?",
        default=False,
    )
    effect_on_electricity_demand_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    communication_goals = models.BooleanField(
        "Werden die Ergebnisse der Zielszenarien inkl. der Möglichkeit zur Kommentierung zugänglich gemacht? Gibt es eine Möglichkeit die Ergebnisse mit der Kommune zu diskutieren?",
        default=False,
    )
    communication_goals_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    designation_of_areas = models.BooleanField(
        "Gibt es eine zeitlich nachvollziehbare Planung für die Ausweisung der Gebiete, d.h. ab wann, welche Gebiete mit welcher Versorgung ausgebaut werden sollen?",
        default=False,
    )
    designation_of_areas_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    criteria_comprehensible = models.BooleanField(
        "Wird dies erklärt bzw. wird deutlich, warum bzw. basierend auf welchen Kriterien (Topographie, Wärmebedarfsdichte, zentrale erneuerbare Wärmequellen etc.)?",
        default=False,
    )
    criteria_comprehensible_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    based_on_analyses = models.BooleanField(
        "Ergibt sich die Einteilung in voraussichtliche Wärmeversorgungsgebiete aufgrund der vorherigen Analysen?",
        default=False,
    )
    based_on_analyses_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    effective_measures = models.BooleanField(
        "Entwickelt die Kommune (bzw. die von ihr beauftragten Akteure) einen aus den Potenzialen und Zielszenario abgeleiteten ambitionierten Transformationspfad mit effektiven Maßnahmen?",
        default=False,
        help_text=mark_safe(
            "<ul><li>Mit klaren Zuständigkeiten der beteiligten Akteure</li><li>Mit jahresscharfer Aktivität</li><li>Mit Fokus auf die wirksamsten Maßnahmen</li><li>Mit einem langfristigen Zeitplan, sodass die Gesamtheit der Maßnahmen im klimaneutralen Zieljahr abgeschlossen werden können (z.B. die lange dauernden Maßnahmen frühzeitig anschieben)</li></ul>"
        ),
    )
    effective_measures_rationale = models.TextField(
        "Begründung",
        blank=True,
    )
    energy_sources_sustainable = models.BooleanField(
        "Basieren die darauffolgend entwickelten Transformationspläne auf den von LocalZero empfohlenen Wärmequellen (und z.B. nicht wesentlich auf Wasserstoff oder Biomasse)?",
        default=False,
        help_text="Auch hier kann die „Wasserstoff-Falle“ wieder zuschnappen. Denn viele Dekarbonisierungsstrategien z.B. von Stadtwerken basieren stark auf Wasserstoff. D.h. auch nach der Wärmeplanung ist es wichtig darauf zu achten, dass Wasserstoff weiter nicht im großen Stile eingesetzt werden soll (also z.B. als Energieträger in den Transformationsplänen der Stadtwerke).",
    )
    energy_sources_sustainable_rationale = models.TextField(
        "Begründung",
        blank=True,
    )


class ExecutionStatus(models.IntegerChoices):
    UNKNOWN = 0, "unbekannt"
    AS_PLANNED = 2, "in Arbeit"
    COMPLETE = 4, "abgeschlossen"
    DELAYED = 6, "verzögert / fehlt"
    FAILED = 8, "gescheitert"


TASK_UNIQUE_CONSTRAINT_NAME = "unique_urls"


class Task(MP_Node):
    """A task to be done to reach climate neutrality or a group of such tasks.

    Tasks form a tree. We use django-treebeard for this.
    `MP_Node` is treebeards base class for all nodes in the tree.

    A group is a node with children and a task is a node without children.

    Some background for the handling of the `slugs` field:
    The tree structure is expected to be reflected in the URL as the directory structure.
    E.g. a task "Windpower" in the task group "Electricity" shall have an
    URL "https://.../electricity/windpower".
    In order to retrieve the required data based on the URL, the complete directory
    is stored in the `slugs` field, e.g. "electricity/windpower".
    The `slugs` field is used together with the `slug` of the city in the URL,
    e.g. "https://.../hamburg/electricity/windpower".
    Therefore it has to be unique per city.

    Usually, e.g. in a blog system, slugs are never updated.
    Here they are updated, since it is quite important to have an URL with the slug based on the current name.
    When the slug is updated, the uniqueness has to be checked again.
    However, when `editable=False` is set, django admin prevents that.
    See clean() and vallidate_unique() for technical details.
    """

    class Meta:
        verbose_name = "Handlungsfeld / Maßnahme"
        verbose_name_plural = "Handlungsfelder und Maßnahmen"
        constraints = [
            models.UniqueConstraint(
                models.F("city"),
                models.F("slugs"),
                name=TASK_UNIQUE_CONSTRAINT_NAME,
            )
        ]

    city = models.ForeignKey(City, on_delete=models.PROTECT)

    draft_mode = models.BooleanField(
        "Entwurfs-Modus",
        default=True,
        help_text=(
            "Im Entwurfs-Modus ist das Handlungsfeld/die Maßnahme für normale Besucher im Frontend"
            " unsichtbar. Nur wenn im gleichen Browser ein User im Admin angemeldet ist, wird"
            " er/sie angezeigt."
        ),
    )

    class TaskSource(models.IntegerChoices):
        CLIMATE_ACTION_PLAN = 0, "KAP"
        SUGGESTED = 1, "Vorschlag"

    source = models.IntegerField(
        "KAP oder eigener Vorschlag?",
        choices=TaskSource.choices,
        default=TaskSource.CLIMATE_ACTION_PLAN,
        help_text=(
            "Stammt dieses Handlungsfeld / diese Maßnahme aus dem bereits vorhandenen Klimaaktions-Plan"
            " oder handelt es sich hierbei um einen Vorschlag eures Lokalteams?"
            " Hinweis: Bei Handlungsfeldern hat dieses Feld aktuell keine Auswirkungen auf die Darstellung und wird ignoriert."
        ),
    )

    frontpage = models.BooleanField(
        "Startseite",
        default=False,
        help_text=(
            "Die Maßahme soll auf der Startseite angezeigt werden, um sie besonders hervorzuheben."
            " Dies funktioniert nur für Maßnahmen und nicht für Handlungsfelder, also nur, wenn"
            " es keine weiteren Untermaßnahmen mehr gibt."
        ),
    )

    title = models.CharField(
        "Titel",
        max_length=50,
        help_text="""
            <p>Überschrift des Handlungsfelds / der Maßnahme.</p>
            <p>Wie im Klimaaktionsplan angegeben oder verkürzt. Maximal 50 Zeichen.</p>
        """,
    )

    teaser = models.CharField(
        "Teaser",
        max_length=200,
        blank=True,
        help_text="""
            <p>Eine kurze Beschreibung des Handlungsfelds / der Maßnahme. Maximal 200 Zeichen. Keine Formatierungen.</p>
            <p>Kann in einer Übersicht mehrerer Handlungsfelder / Maßnahmen oder als Vorschau eines Links dargestellt werden.</p>
        """,
    )

    # 1. Beschreibung: Inhalte aus dem KAP

    description = models.TextField(
        "Beschreibung",
        blank=True,
        help_text="""
            <p>Texte aus dem Klimaaktionsplan können hier eins-zu-eins eingegeben werden.</p>
            <p>Für Handlungsfelder sind Einleitungstexte aus dem Plan geeignet.</p>
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

    responsible_organ = models.CharField(
        "Verantwortliches Organ",
        blank=True,
        max_length=200,
        help_text="Name oder gebräuchliche Abkürzung des verantwortlichen Gremiums oder Behörde",
    )

    responsible_organ_explanation = models.TextField(
        "Erklärungstext zum verantwortlichen Organ",
        blank=True,
        help_text="""
            <p>Ausgeschriebener Name, falls eine Abkürzung für das verantwortliche Organ verwendet wurde.</p>
            <p>Eventuell Ansprechperson oder Kontaktdaten, wenn diese öffentlich zugänglich sind.</p>
            <p>Gegebenenfalls eine Begründung, warum es an diesem Organ hängt.</p>
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

    execution_status = models.IntegerField(
        "Umsetzungsstand",
        choices=ExecutionStatus.choices,
        default=ExecutionStatus.UNKNOWN,
        help_text="""
            <p>Bei Maßnahmen: Wird/wurde die Maßnahme wie geplant umgesetzt?</p>
            <dl>
                <dt>unbekannt</dt><dd><ul>
                    <li>Keine Infos vorhanden</li>
                    <li>Es gibt einen unkonkreten Beschluss</li>
                </ul></dd>
                <dt>in Arbeit</dt><dd><ul>
                    <li>Finden wir erstmal gut: Dinge werden bearbeitet.</li>
                    <li>Maßnahmen, die im Zeitplan sind (sowohl begonnen als auch in Planung).</li>
                    <li>Maßnahmen die in Umsetzung sind.</li>
                    <li>Maßnahmen für die es einen positiven Beschluss + Zeitplan (Konkretisierung) gibt.</li>
                </ul></dd>
                <dt>abgeschlossen</dt><dd><ul>
                    <li>Top und im Plan fertig.</li>
                </ul></dd>
                <dt>verzögert / fehlt</dt><dd><ul>
                    <li>Maßnahmen, die nicht im Zeitplan sind.</li>
                    <li>Maßnahmen, die im Prinzip noch vervollständigt werden können.</li>
                    <li>Maßnahmen, die im KAP nicht aufgeführt sind, (und nicht bearbeitet weden)</li>
                    <li>Im Prinzip könnten sie aber noch angegangen werden.</li>
                </ul></dd>
                <dt>gescheitert</dt><dd><ul>
                    <li>Kann niemals mehr geschafft werden (Eiche ist gefällt, Moor ist mit einer Autobahn überbaut)</li>
                    <li>Sowohl für Maßnahmen aus dem KAP, als auch Dinge, die gar nich im KAP aufgeführt waren.</li>
                </ul></dd>
            </dl>
            <p>Bei Handlungsfeldern:</p>
            <p>Wenn hier "unbekannt" ausgewählt wird, werden die Umsetzungsstände der Maßnahmen in diesem Handlungsfeld zusammengefasst.</p>
            <p>Bei anderen Auswahlen wird diese Zusammenfassung überschrieben. Das sollte nur passieren, wenn sie unpassend oder irreführend ist.</p>
        """,
    )

    execution_justification = models.TextField(
        "Begründung Umsetzungsstand",
        blank=True,
        help_text="Die Auswahl bei Umsetzungsstand kann hier ausführlich begründet werden.",
    )

    supporting_ngos = models.TextField(
        "Unterstützung von",
        blank=True,
        help_text="hier kann die Unterstüzung von anderen NGOs gewürdigt werden",
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
        "Tatsächliches Ende",
        blank=True,
        null=True,
        help_text="Nur falls bekannt.",
    )

    internal_information = models.TextField(
        "Interne Informationen",
        blank=True,
        help_text="""
            <p>Interne Informationen, Notizen, Referenzen etc.</p>
            <p>Die hier angegebenen Informationen werden nur in der Admin-Oberfläche angezeigt und nicht im Frontend.</p>
        """,
    )

    def __str__(self) -> str:
        return self.title

    slugs = models.SlugField(
        "In der URL",
        max_length=255,
        editable=False,
    )

    @staticmethod
    def _get_slugs_with_parent(new_parent, title):
        """Determine the `slugs` field based on the new parents slugs and title."""
        if new_parent:
            return new_parent.slugs + "/" + slugify(title)
        else:
            return slugify(title)

    @staticmethod
    def get_slugs_for_move(ref_node, pos, title):
        """Determine the `slugs` field given treebeards reference data `ref_node` and `pos`.

        Some values of `pos` mean a position as sibling of ref_node and others
        as child. The latter all end with "-child".
        """
        if ref_node and isinstance(pos, str) and not pos.endswith("-child"):
            # The (new) position is not child of `ref_node`, it is a sibling.
            new_parent = ref_node.get_parent()
        else:
            # The (new) position is a child of `ref_node` -> `ref_node` is the parent.
            new_parent = ref_node
        return Task._get_slugs_with_parent(new_parent, title)

    def validate_constraints(self, exclude=None):
        """
        Add slugs to fields to validate uniqueness and convert to a more readable error.

        This is necessary, because `editable=False` excludes the field from validation
        and UniqueConstraint does not allow error messages showing content.
        """

        if exclude:
            if "slugs" in exclude:
                exclude.remove("slugs")
            if "city" in exclude:
                exclude.remove("city")
        try:
            super().validate_constraints(exclude=exclude)
        except ValidationError as e:
            new_msg = (
                "Das Handlungsfeld / die Maßnahme wird in der URL als '%(slugs)s' geschrieben."
                " Das kollidiert mit einem anderen Eintrag." % {"slugs": self.slugs}
            )
            msgs: dict[str, str] = e.message_dict
            msgs[NON_FIELD_ERRORS][:] = [
                new_msg if TASK_UNIQUE_CONSTRAINT_NAME in msg else msg
                for msg in msgs[NON_FIELD_ERRORS]
            ]
            raise ValidationError(msgs)

    def move(self, target, pos=None):
        """Override to validate uniqueness of slugs field in case of move in changelist.

        It is necessary to update the `slugs` field of the moved node (but not its chilrden)
        in order to ensure the uniqueness is fulfilled at the new position, before the move is
        performed.

        It might also be possible to override `treebeard.admin.TreeAdmin.try_to_move_node()`,
        instead. This would possibly catch more cases.
        """

        self.slugs = self.get_slugs_for_move(target, pos, self.title)
        try:
            self.validate_constraints()
        except ValidationError as e:
            raise InvalidPosition(
                "Diese Verschiebung ist nicht möglich."
                " Es gibt bereits ein Handlungsfeld / eine Maßnahme"
                " mit der URL '%s'." % self.slugs
            )
        super().move(target, pos)

    def save(self, *args, **kwargs):
        """Override to correct `slugs` of whole sub-tree after move or rename.

        Calls itself recursively for all descendants after the regular save.
        It is important to do the recursion after `super().save()`: This way
        the children can use the `slugs` field of the parent to update their `slugs` field.

        Any move within the tree structure has to happen before, such that
        `get_parent()` returns the correct parent. Treebeard first moves, then saves.
        """

        self.slugs = self._get_slugs_with_parent(self.get_parent(), self.title)
        super().save(*args, **kwargs)
        for child in self.get_children().only("slugs", "title"):
            child.save()

    def get_execution_status_name(self):
        for s in ExecutionStatus:
            if s.value == self.execution_status:
                return s.name
        return ""

    @property
    def started_late(self):
        return (
            self.planned_start
            and self.actual_start
            and self.planned_start < self.actual_start
        )

    @property
    def completed_late(self):
        return self.planned_completion and (
            not self.actual_completion
            and self.planned_completion < date.today()
            or self.actual_completion
            and self.planned_completion < self.actual_completion
        )

    @property
    def is_suggestion(self):
        return self.source == self.TaskSource.SUGGESTED

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


class Chart(models.Model):
    class Meta:
        verbose_name = "Diagramm"
        verbose_name_plural = "Diagramme"

    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="charts")
    image = models.ImageField("Bilddatei", upload_to="uploads/%Y/%m/%d/")
    alt_description = models.CharField(
        "Beschreibung (für Menschen, die das Bild nicht sehen können)", max_length=255
    )
    source = models.CharField("Quelle", max_length=255)
    license = models.CharField("Lizenz", max_length=255)
    caption = models.TextField("Bildunterschrift")

    internal_information = models.TextField(
        "Interne Informationen",
        blank=True,
        help_text="""
            <p>Interne Informationen, Notizen, Referenzen etc.</p>
            <p>Die hier angegebenen Informationen werden nur in der Admin-Oberfläche angezeigt und nicht im Frontend.</p>
        """,
    )

    def __str__(self) -> str:
        return self.alt_description + " - Quelle: " + self.source

    def save(self):
        super().save()

        # limit image size to max 2000 width or height (keeps aspect ratio)
        img = Image.open(self.image.path)
        if img.width > 2000 or img.height > 2000:
            img.thumbnail((2000, 2000))
            img.save(self.image.path)


class LocalGroup(models.Model):
    class Meta:
        verbose_name = "Lokalgruppe"
        verbose_name_plural = "Lokalgruppen"

    city = models.OneToOneField(
        City, on_delete=models.PROTECT, related_name="local_group"
    )
    name = models.CharField(
        max_length=100,
        help_text="""
            <p>Offizieller Name der Lokalgruppe. Maximal 100 Zeichen.</p>
        """,
    )
    website = models.URLField(
        blank=True,
        help_text="""
            <p>URL der Website der Lokalgruppe.</p>
        """,
    )
    teaser = models.CharField(
        "Teaser",
        max_length=200,
        blank=True,
        help_text="""
            <p>Eine kurze Beschreibung der Lokalgruppe. Maximal 200 Zeichen. Keine Formatierungen.</p>
        """,
    )
    description = models.TextField(
        "Beschreibung",
        blank=True,
        help_text="""
            <p>Details über die Lokalgruppe. Sollte mindestens eine Kontaktmöglichkeit enthalten sowie
            Angaben darüber, wie die Gruppe das Monitoring durchführt (Datenquellen? Gesprächspartner?
            Als Geschichte erzählt). Mögliche weitere Infos (sofern das nicht alles ohnehin schon
            auf der Website der Gruppe steht):</p>
            <ul>
            <li>Ehrenamtliche, Aktuelle Zahl, Zur Verfügung stehende Zeit. (Ziel: Erwartungsmanagement)</li>
            <li>Beteiligungsmöglichkeiten</li>
            <li>ggf. Hintergrund zum Klimaaktionsplan? Wie war unser Weg dahin?</li>
            </ul>
        """,
    )
    logo_square = models.ImageField(
        "quadratisches Logo",
        blank=True,
        upload_to="uploads/%Y/%m/%d/",
        help_text="""
            <p>Logo eurer Kommune für die Kommunenliste.
            Am besten quadratisch und weiß auf transparent,
            da es auf gelbem Hintergrund angezeigt wird.</p>
        """,
    )
    logo_wide = models.ImageField(
        "breites Logo",
        blank=True,
        upload_to="uploads/%Y/%m/%d/",
        help_text="""
            <p>Logo für die Hauptseite eurer Kommune.
            Am besten nicht weiß, da es auf weißem Hintergrund angezeigt wird.</p>
        """,
    )
    featured_image = models.ImageField(
        "Foto der Lokalgruppe",
        blank=True,
        upload_to="uploads/%Y/%m/%d/",
        help_text="Mindestens 500 Pixel breit und 300 Pixel hoch.",
    )

    def save(self):
        super().save()

        if self.featured_image:
            # limit featured_image size to max 1000 width or height (keeps aspect ratio)
            img = Image.open(self.featured_image.path)
            if img.width > 1000 or img.height > 1000:
                img.thumbnail((1000, 1000))
                img.save(self.featured_image.path)


class AccessRight(models.TextChoices):
    CITY_ADMIN = "city admin", "Kommunen-Administrator"
    CITY_EDITOR = "city editor", "Kommunen-Bearbeiter"


class Invitation(AbstractBaseInvitation):
    """
    Invitation suitable to be send as link without email, but with rights attached.
    Invitations will be created automatically, whenever a city is saved. No user will
    have to add invitations by hand. They can only be deleted to invalidate links.
    New links will be created upon the next save of the city.
    """

    class Meta:
        verbose_name = "Einladungslink"
        verbose_name_plural = "Einladungslinks"

    city = models.ForeignKey(
        City,
        verbose_name="Kommune",
        on_delete=models.CASCADE,
        related_name="invitations",
    )
    access_right = models.CharField(
        "Zugriffsrecht",
        max_length=20,
        choices=AccessRight.choices,
        default=AccessRight.CITY_EDITOR,
    )

    created = models.DateTimeField(
        verbose_name="Erstellungszeitpunkt", default=timezone.now
    )

    @property
    def email(self):
        "Satisfy expected interface."
        return f"{self.get_access_right_display()} von {self.city.name}"

    @classmethod
    def create_for_right(cls, city, access_right):
        "Create a new invitation for a city with a given right."
        key = get_random_string(64).lower()
        return cls._default_manager.create(
            key=key, inviter=None, city=city, access_right=access_right
        )

    @classmethod
    def ensure_for_right(cls, city, access_right):
        "Ensure there exists an invitation for a city with a given right."
        if not cls._default_manager.filter(city=city, access_right=access_right):
            cls.create_for_right(city, access_right)

    @classmethod
    def ensure_for_city(cls, city):
        "Ensure there exist the needed invitations for a city."
        cls.ensure_for_right(city, AccessRight.CITY_EDITOR)
        cls.ensure_for_right(city, AccessRight.CITY_ADMIN)

    @classmethod
    def create(cls, email, inviter=None, **kwargs):
        "Implementation of required method. Not used."
        key = get_random_string(64).lower()
        return cls._default_manager.create(
            email=email, key=key, inviter=inviter, **kwargs
        )

    def get_invite_url(self, request):
        """
        Build correct URL to be sent to invited users.
        Extracted from django-invitations, which generates it for the email and forgets it.
        """
        if not self.key:
            return None
        url = reverse(invitations_app_settings.CONFIRMATION_URL_NAME, args=[self.key])
        return request.build_absolute_uri(url)

    def key_expired(self):
        "Implementation of required method. Never expired."
        return False

    def send_invitation(self, request, **kwargs):
        "Implementation of required method. Pretending to send an email."
        self.sent = timezone.now()
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=self.get_invite_url(request),
            inviter=self.inviter,
        )

    def __str__(self):
        return f"Einladung für {self.get_access_right_display()} von {self.city.name}"


def get_invitation(request: HttpRequest) -> Invitation | NoneType:
    "Retrieve an invitation based on the key in the current session."
    if not hasattr(request, "session"):
        return None
    key = request.session.get("invitation_key")
    if not key:
        return None
    invitation_qs = Invitation.objects.filter(key=key.lower())
    if not invitation_qs:
        return None
    return invitation_qs.first()


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
