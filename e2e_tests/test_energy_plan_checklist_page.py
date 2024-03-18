from playwright.sync_api import Page, expect


def test_should_show_the_heading_and_subheadings_regarding_the_energy_plan(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/waermeplanung_checkliste/")

    expect(page.get_by_role("heading", name="Wärmeplanung", exact=True)).to_be_visible()
    expect(page.get_by_text("1. Beschluss zur Durchführung")).to_be_visible()
    expect(
        page.get_by_text(
            "7. Umsetzungsstrategie und konkrete Umsetzungsmaßnahmen (§ 20)"
        )
    ).to_be_visible()


def test_should_expand_the_rationale_when_clicking_on_a_checklist_item(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/waermeplanung_checkliste/")

    checklist_item = page.get_by_role(
        "button",
        name="Liegt ein öffentlich bekannt gemachter Beschluss zur Durchführung der Wärmeplanung vor?",
    )
    rationale = page.locator(
        ".accordion-collapse",
        has_text="Ja zu finden unter [1].",
    )

    expect(rationale).not_to_be_visible()

    checklist_item.click()

    expect(rationale).to_be_visible()
