from playwright.sync_api import Page, expect


def test_should_redirect_to_the_city_page_when_clicking_the_back_button(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/verwaltungsstrukturen_checkliste/")

    page.get_by_text("Zurück").click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/")


def test_should_show_the_administration_assessment_and_the_checklist(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/verwaltungsstrukturen_checkliste/")

    expect(
        page.locator(
            ".card",
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
    ).to_have_class("lz-icon CROSSED")
