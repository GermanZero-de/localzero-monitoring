from playwright.sync_api import Page, expect


def test_should_show_the_administration_assessment_and_the_checklist(
    live_server, page: Page
):
    page.goto(
        live_server.url + "/deutschland/beispielstadt/verwaltungsstrukturen_checkliste/"
    )

    expect(
        page.locator(
            "p",
            has_text="Wie bewertet ihr die Nachhaltigkeitsarchitektur der Verwaltung? Dieser Text fasst die wichtigsten Punkte zusammen.",
        )
    ).to_be_visible()

    expect(
        page.locator(
            "tr",
            has=page.locator(
                'td:text("Gibt es ein Monitoring von Kimaschutzmaßnahmen?")'
            ),
        )
        .locator("td", has=page.locator("svg"))
        .locator("svg")
    ).to_have_class("lz-icon CHECKED")

    expect(
        page.locator(
            "tr",
            has=page.locator(
                'td:text("Gibt es Richtlinien für ein nachhaltiges Beschaffungswesen?")'
            ),
        )
        .locator("td", has=page.locator("svg"))
        .locator("svg")
    ).to_have_class("lz-icon EMPTY")


def test_should_expand_the_help_text_and_rationale_when_clicking_on_a_checklist_item(
    live_server, page: Page
):
    page.goto(
        live_server.url + "/deutschland/beispielstadt/verwaltungsstrukturen_checkliste/"
    )

    checklist_item = page.get_by_role(
        "button",
        name="Gibt es ein Monitoring von Kimaschutzmaßnahmen?",
    )
    help_text = page.locator(
        ".accordion-collapse",
        has_text="Monitoring bedeutet ein Überwachen/Überblick über den Erfolg von Klimaschutzmaßnahmen.",
    )
    rationale = page.locator(
        ".accordion-collapse",
        has_text="Das Monitoring kann hier eingesehen werden:",
    )

    expect(help_text).not_to_be_visible()
    expect(rationale).not_to_be_visible()

    checklist_item.click()

    expect(help_text).to_be_visible()
    expect(rationale).to_be_visible()


def test_should_only_expand_the_latest_helptext_when_clicking_on_two_different_checklist_items(
    live_server, page: Page
):
    page.goto(
        live_server.url + "/deutschland/beispielstadt/verwaltungsstrukturen_checkliste/"
    )

    checklist_item1 = page.get_by_role(
        "button",
        name="Gibt es ein Monitoring von Kimaschutzmaßnahmen?",
    )
    help_text1 = page.locator(
        ".accordion-collapse",
        has_text="Monitoring bedeutet ein Überwachen/Überblick über den Erfolg von Klimaschutzmaßnahmen.",
    )

    checklist_item2 = page.get_by_role(
        "button",
        name="Gibt es Richtlinien für ein nachhaltiges Beschaffungswesen?",
    )
    help_text2 = page.locator(
        ".accordion-collapse",
        has_text="Die Kommunalverwaltung kann aufgrund ihres großen Beschaffungsvolumens mit ihrer Nachfrage energieeffiziente Produkte fördern",
    )

    checklist_item1.click()
    checklist_item2.click()

    expect(help_text1).not_to_be_visible()
    expect(help_text2).to_be_visible()
