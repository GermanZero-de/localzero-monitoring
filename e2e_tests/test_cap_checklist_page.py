from playwright.sync_api import Page, expect


def test_should_show_the_cap_assessment_and_the_checklist(live_server, page: Page):
    page.goto(live_server.url + "/deutschland/beispielstadt/kap_checkliste/")

    expect(
        page.locator(
            "p",
            has_text="Hier soll die Bewertung des Klimaaktionsplans stehen. Was haltet ihr von dem Plan?",
        )
    ).to_be_visible()

    expect(
        page.locator(
            "tr",
            has=page.locator(
                'td:text("Ist im Klima-Aktionsplan ein Zieljahr der Klimaneutralität hinterlegt, das vom höchsten kommunalen Gremium beschlossen wurde?")'
            ),
        )
        .locator("td", has=page.locator("svg"))
        .locator("svg")
    ).to_have_class("lz-icon CHECKED")

    expect(
        page.locator(
            "tr",
            has=page.locator(
                'td:text("Enthält der Klima-Aktionsplan ein Szenario mit dem Ziel Klimaneutralität bis 2035?")'
            ),
        )
        .locator("td", has=page.locator("svg"))
        .locator("svg")
    ).to_have_class("lz-icon EMPTY")


def test_should_expand_the_help_text_and_rationale_when_clicking_on_a_checklist_item(
    live_server, page: Page
):
    page.goto(live_server.url + "/deutschland/beispielstadt/kap_checkliste/")

    checklist_item = page.get_by_role(
        "button",
        name="Ist ein Trendszenario hinterlegt?",
    )
    help_text = page.locator(
        ".accordion-collapse",
        has_text="Ein Trendszenario zeigt auf, wie sich die kommunalen Emissionen entwickeln",
    )
    rationale = page.locator(
        ".accordion-collapse",
        has_text="Trendszenario ist in Arbeit",
    )

    expect(help_text).not_to_be_visible()
    expect(rationale).not_to_be_visible()

    checklist_item.click()

    expect(help_text).to_be_visible()
    expect(rationale).to_be_visible()


def test_should_only_expand_the_latest_helptext_when_clicking_on_two_different_checklist_items(
    live_server, page: Page
):
    page.goto(live_server.url + "/deutschland/beispielstadt/kap_checkliste/")

    checklist_item1 = page.get_by_role(
        "button",
        name="Bilanziert der Klima-Aktionsplan in den Sektoren der Klimavision?",
    )
    help_text1 = page.locator(
        ".accordion-collapse",
        has_text="Die Klimavision beinhaltet die Sektoren Strom, Wärme, Verkehr, Industrie, Gebäude, Abfall",
    )

    checklist_item2 = page.get_by_role(
        "button",
        name="Enthält der Klima-Aktionsplan ein Szenario mit dem Ziel Klimaneutralität bis 2035?",
    )
    help_text2 = page.locator(
        ".accordion-collapse",
        has_text="Das Szenario soll zeigen wie die Kommune unter realistischen Bedinungen",
    )

    checklist_item1.click()
    checklist_item2.click()

    expect(help_text1).not_to_be_visible()
    expect(help_text2).to_be_visible()
