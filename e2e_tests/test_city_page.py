from playwright.sync_api import Page, expect


def test_should_go_to_city_view_when_clicking_city_select_dropdown_item(
    live_server, page: Page
):
    page.goto(live_server.url)

    city_select_button = page.get_by_text("Stadt auswählen")
    city_select_button.click()

    city_button = page.get_by_text("Beispielstadt")
    city_button.click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/")


def test_city_page_should_have_city_name_in_title(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/")

    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_should_go_to_tasks_view_when_clicking_on_the_tasks_card(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/")

    page.get_by_text("Maßnahmen offen").click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/massnahmen/")


def test_should_go_to_the_administration_checklist_view_when_clicking_the_checklist_card(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/")

    page.get_by_text("Verwaltungsstrukturen").click()

    expect(page).to_have_url(
        live_server.url + "/beispielstadt/verwaltungsstrukturen_checkliste/"
    )
