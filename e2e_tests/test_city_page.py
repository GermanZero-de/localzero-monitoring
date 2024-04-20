from playwright.sync_api import Page, expect
import re


def test_should_go_to_city_view_when_clicking_city_select_dropdown_item(
    live_server, page: Page
):
    page.goto(live_server.url)

    city_select_button = page.get_by_role("button", name="Kommunen")
    city_select_button.click()

    city_button = page.locator(".sub-menu .menu-item", has_text="Beispielstadt")
    city_button.click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/")


def test_city_page_should_have_city_name_in_title(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/")

    expect(page).to_have_title("Beispielstadt - Monitoring LocalZero")


def test_all_city_related_pages_should_show_the_city_logo(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/")

    expect(
        page.get_by_role("img", name="Logo der Lokalgruppe BeispielLos")
    ).to_be_visible()

    page.goto(live_server.url + "/beispielstadt/kap_checkliste/")

    expect(
        page.get_by_role("img", name="Logo der Lokalgruppe BeispielLos")
    ).to_be_visible()

    page.goto(live_server.url + "/beispielstadt/verwaltungsstrukturen_checkliste/")

    expect(
        page.get_by_role("img", name="Logo der Lokalgruppe BeispielLos")
    ).to_be_visible()

    page.goto(live_server.url + "/beispielstadt/waermeplanung_checkliste/")

    expect(
        page.get_by_role("img", name="Logo der Lokalgruppe BeispielLos")
    ).to_be_visible()

    page.goto(live_server.url + "/beispielstadt/massnahmen/mobilitat/")

    expect(
        page.get_by_role("img", name="Logo der Lokalgruppe BeispielLos")
    ).to_be_visible()

    page.goto(
        live_server.url
        + "/beispielstadt/massnahmen/mobilitat/u-bahn-strecke-verlangern/"
    )

    expect(
        page.get_by_role("img", name="Logo der Lokalgruppe BeispielLos")
    ).to_be_visible()


def test_city_page_should_display_supporting_ngos(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/")

    expect(page.get_by_text("Mit Unterstützung von")).to_be_visible()
    expect(page.get_by_role("link", name="aidfive")).to_be_visible()


def test_city_page_should_not_contain_internal_information(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/")

    expect(page.locator(".page-body")).not_to_contain_text(
        "Dies ist eine total wichtige interne Info!"
    )


def test_should_go_to_tasks_view_when_clicking_on_the_tasks_card(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/")

    page.get_by_text("Maßnahmen offen").click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/massnahmen/")


def test_should_go_to_the_cap_checklist_view_when_clicking_the_cap_checklist_card(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/")

    page.get_by_text("Klimaaktionsplan").click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/kap_checkliste/")


def test_should_go_to_the_administration_checklist_view_when_clicking_the_checklist_card(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/")

    page.get_by_text("Verwaltungsstrukturen").click()

    expect(page).to_have_url(
        live_server.url + "/beispielstadt/verwaltungsstrukturen_checkliste/"
    )


def test_should_display_years_and_days_when_more_than_365_days(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/")

    expect(
        page.get_by_text(re.compile("Noch [0-9]+ Jahre und [0-9]+ Tage"))
    ).to_be_visible()


def test_should_display_only_days_when_less_than_365_days(live_server, page: Page):
    page.goto(live_server.url + "/mitallem/")

    expect(page.get_by_text(re.compile("Noch [0-9]+ Tage"))).to_be_visible()
    expect(
        page.get_by_text(re.compile("Noch [0-9]+ Jahre und [0-9]+ Tage"))
    ).not_to_be_visible()
