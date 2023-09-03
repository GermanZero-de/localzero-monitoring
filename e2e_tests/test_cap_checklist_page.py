from playwright.sync_api import Page, expect


def test_should_show_the_cap_assessment_and_the_checklist(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/kap_checkliste/")

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
                'td:text("Ist im KAP ein Zieljahr der Klimaneutralität hinterlegt, das vom höchsten kommunalen Gremium beschlossen wurde?")'
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


def test_should_show_the_correct_helptext_for_cap_assessment(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/kap_checkliste/")
    checked_question_button = page.locator(
        "button",
        has=page.locator(
            'td:text("Ist im KAP ein Zieljahr der Klimaneutralität hinterlegt, das vom höchsten kommunalen Gremium beschlossen wurde?")'
        ),
    )
    checked_question_help_text_locator = page.locator(
        checked_question_button.get_attribute("data-bs-target")
    )
    unchecked_question_button = page.locator(
        "button",
        has=page.locator(
            'td:text("Enthält der Klima-Aktionsplan ein Szenario mit dem Ziel Klimaneutralität bis 2035?")'
        ),
    )
    unchecked_question_help_text_locator = page.locator(
        unchecked_question_button.get_attribute("data-bs-target")
    )

    expect(checked_question_help_text_locator).to_contain_text(
        "Dies sorgt dafür, dass nicht nur Emissionen gemindert werden,"
        " sondern, ein klares Ziel bis z.B. 2035 gesetzt wird bis wann die Kommune"
        " möglichst ohne Kompensation klimaneutral (keine Emissionen vom Gebiet der Gemeinde) werden soll.\n"
        "Mit höchstes Gremium ist hier gemeint z.B. der Stadtrat oder Gemeinderat."
    )

    # Help-Text not visible before clicking for CHECKED
    expect(checked_question_help_text_locator).to_be_hidden()

    # Help-Text visible after clicking for CHECKED
    checked_question_button.click()
    expect(checked_question_help_text_locator).to_be_visible()

    expect(unchecked_question_help_text_locator).to_contain_text(
        "Das Szenario soll zeigen wie die Kommune unter realistischen Bedinungen"
        " (politischer Entwicklung, Dauer der Maßnahmen etc.) ihre Emissionen auf Netto-Null"
        " reduzieren kann, oder wie weit eine Reduktion realistisch aber ambitioniert möglich ist."
    )

    # Other Help-Text not visible for UNCHECKED
    expect(unchecked_question_help_text_locator).to_be_hidden()

    # After Click Help-Text for UNCHECKED visible
    unchecked_question_button.click()
    expect(unchecked_question_help_text_locator).to_be_visible()

    # First one should be not visible again
    expect(checked_question_help_text_locator).to_be_hidden()


def test_should_expand_and_unexpand_the_help_text_when_clicking_on_a_checklist_item(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/kap_checkliste/")

    checklist_item = page.get_by_role(
        "button",
        name="Bilanziert der Klima-Aktionsplan in den Sektoren der Klimavision?",
    )
    help_text = page.locator(
        ".accordion-collapse",
        has_text="Die Klimavision beinhaltet die Sektoren Strom, Wärme, Verkehr, Industrie, Gebäude, Abfall",
    )

    expect(help_text).not_to_be_visible()

    checklist_item.click()

    expect(help_text).to_be_visible()


def test_should_only_expand_the_last_helptext_when_clicking_on_two_checklist_items(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/kap_checkliste/")

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
