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
            'td:text("Gibt es ein Monitoring von Kimaschutzmaßnahmen?") + td'
        ).locator("svg")
    ).to_have_class("lz-icon CHECKED")
    expect(
        page.locator(
            'td:text("Gibt es Richtlinien für ein nachhaltiges Beschaffungswesen?") + td'
        ).locator("svg")
    ).to_have_class("lz-icon EMPTY")
