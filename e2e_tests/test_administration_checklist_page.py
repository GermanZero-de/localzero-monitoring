from playwright.sync_api import Page, expect


def test_should_show_the_administration_assessment_and_the_checklist(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/verwaltungsstrukturen_checkliste/")

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


def test_should_show_the_correct_helptext_for_administration_assessment(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/verwaltungsstrukturen_checkliste/")
    checked_question_button = page.locator(
        "button",
        has=page.locator('td:text("Gibt es ein Monitoring von Kimaschutzmaßnahmen?")'),
    )
    checked_question_help_text_locator = page.locator(
        checked_question_button.get_attribute("data-bs-target")
    )
    unchecked_question_button = page.locator(
        "button",
        has=page.locator(
            'td:text("Gibt es Richtlinien für ein nachhaltiges Beschaffungswesen?")'
        ),
    )
    unchecked_question_help_text_locator = page.locator(
        unchecked_question_button.get_attribute("data-bs-target")
    )

    expect(checked_question_help_text_locator).to_contain_text(
        "Monitoring bedeutet ein Überwachen / Überblick über den Erfolg von Klimaschutzmaßnahmen."
        " Dieser kann in eingespaarten Emissionen sichtbar gemacht werden und ist wichtig um das Ziel der Klimaneutralität"
        " und notwendige Schritte im Auge zu behalten."
    )

    # Help-Text not visible before clicking for CHECKED
    expect(checked_question_help_text_locator).to_be_hidden()

    # Help-Text visible after clicking for CHECKED
    checked_question_button.click()
    expect(checked_question_help_text_locator).to_be_visible()

    expect(unchecked_question_help_text_locator).to_contain_text(
        "Die Kommunalverwaltung kann aufgrund ihres großen Beschaffungsvolumens mit ihrer Nachfrage energieeffiziente Produkte fördern"
        " und damit einen wichtigen Beitrag zum Klimaschutz leisten. Wichtig ist, möglichst nur Produkte und Dienstleistungen zu erwerben,"
        " die wirklich benötigt werden und im Sinne der Nachhaltigkeit neben einer hohen Umweltverträglichkeit auch sozialen wie ökonomischen"
        " Aspekten entsprechen. Umweltfreundliche Beschaffung sollte in grundlegenden Dokumenten der Behörde wie dem eigenen Leitbild,"
        " verpflichtenden Dienstanweisungen oder einem Beschaffungsleitfaden als Organisationsziel definiert werden."
    )

    # Other Help-Text not visible for UNCHECKED
    expect(unchecked_question_help_text_locator).to_be_hidden()

    # After Click Help-Text for UNCHECKED visible
    unchecked_question_button.click()
    expect(unchecked_question_help_text_locator).to_be_visible()

    # First one should be not visible again
    expect(checked_question_help_text_locator).to_be_hidden()
