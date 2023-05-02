from playwright.sync_api import Page, expect


def test_the_task_page_should_have_the_city_name_in_the_title(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/mobilitat/")

    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_should_go_to_subtask_view_when_clicking_task_item(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/mobilitat/")

    subtask_title = page.get_by_text("Radwege ausbauen")
    subtask_title.click()

    expect(page).to_have_url(
        live_server.url + "/beispielstadt/mobilitat/radwege-ausbauen/"
    )
