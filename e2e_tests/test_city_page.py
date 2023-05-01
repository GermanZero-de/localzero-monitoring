from playwright.sync_api import Page, expect


def test_should_go_to_city_view_when_clicking_city_select_dropdown_item(
    django_db_setup, live_server, page: Page
):
    page.goto(live_server.url)

    city_select_button = page.get_by_text("Stadt auswählen")
    city_select_button.click()

    city_button = page.get_by_text("Beispielstadt")
    city_button.click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/")


def test_city_page_should_have_city_name_in_title(
    django_db_setup, live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/")

    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_should_go_to_task_view_when_clicking_task_item(
    django_db_setup, live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/")

    task_title = page.get_by_text("Mobilität")
    task_title.click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/mobilitat/")
