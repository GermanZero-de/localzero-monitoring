from playwright.sync_api import Page, expect


def test_should_show_the_cap_assessment_and_the_checklist(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/kap_checkliste/")

    expect(
        page.locator(
            ".card",
            has_text="Hier soll die Bewertung des Klimaaktionsplans stehen. Was haltet ihr von dem Plan?",
        )
    ).to_be_visible()

    expect(
        page.locator(
            'td:text("Ist im KAP ein Zieljahr der Klimaneutralität hinterlegt und wurde das vom höchsten kommunalen Gremium beschlossen?") + td'
        ).locator("svg")
    ).to_have_class("lz-icon CHECKED")
    expect(
        page.locator(
            'td:text("Enthält der KAP ein Szenario mit dem Ziel Klimaneutralität bis 2035?") + td'
        ).locator("svg")
    ).to_have_class("lz-icon CROSSED")
