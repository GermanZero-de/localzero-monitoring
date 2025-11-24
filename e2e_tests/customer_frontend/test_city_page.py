from playwright.sync_api import Page, expect
import pytest
import re


def test_the_city_page_should_have_the_city_name_in_the_title(
    base_url: str, page: Page
):
    page.goto(base_url + "/beispielstadt/")

    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_all_city_related_pages_should_show_the_city_logo(base_url: str, page: Page):
    logo_name = "Logo von Beispielstadt"
    page.goto(base_url + "/beispielstadt/")

    expect(page.get_by_role("img", name=logo_name)).to_be_visible()

    page.goto(base_url + "/beispielstadt/kap_checkliste/")

    expect(page.get_by_role("img", name=logo_name)).to_be_visible()

    page.goto(base_url + "/beispielstadt/verwaltungsstrukturen_checkliste/")

    expect(page.get_by_role("img", name=logo_name)).to_be_visible()

    page.goto(base_url + "/beispielstadt/waermeplanung_checkliste/")

    expect(page.get_by_role("img", name=logo_name)).to_be_visible()


def test_city_page_should_display_supporting_ngos(base_url: str, page: Page):
    page.goto(base_url + "/beispielstadt/")

    expect(page.get_by_text("Mit Unterstützung von")).to_be_visible()
    expect(page.get_by_role("link", name="aidfive")).to_be_visible()


def test_city_page_should_not_contain_internal_information(base_url: str, page: Page):
    page.goto(base_url + "/beispielstadt/")

    expect(
        page.get_by_text("Dies ist eine total wichtige interne Info!")
    ).to_have_count(0)


def test_should_go_to_tasks_view_when_clicking_on_the_tasks_card(
    base_url: str, page: Page
):
    page.goto(base_url + "/beispielstadt/")

    page.get_by_text("Stand der Maßnahmen").click()

    expect(page).to_have_url(base_url + "/beispielstadt/massnahmen")


def test_should_go_to_the_cap_checklist_view_when_clicking_the_cap_checklist_card(
    base_url: str, page: Page
):
    page.goto(base_url + "/beispielstadt/")

    page.get_by_text("Klimaaktionsplan (KAP)").click()

    expect(page).to_have_url(base_url + "/beispielstadt/kap_checkliste")


def test_should_go_to_the_administration_checklist_view_when_clicking_the_checklist_card(
    base_url: str, page: Page
):
    page.goto(base_url + "/beispielstadt/")

    page.get_by_text("Wo steht die Verwaltung?").click()

    expect(page).to_have_url(
        base_url + "/beispielstadt/verwaltungsstrukturen_checkliste"
    )


def test_should_go_to_the_heatplanning_checklist_view_when_clicking_the_checklist_card(
    base_url: str, page: Page
):
    page.goto(base_url + "/beispielstadt/")

    page.get_by_text("Wärmeplanung").click()

    expect(page).to_have_url(base_url + "/beispielstadt/waermeplanung_checkliste")
