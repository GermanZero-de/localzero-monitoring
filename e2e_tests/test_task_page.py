from playwright.sync_api import Page, expect


def test_task_page_should_have_city_name_and_task_title_in_title(
    page: Page, django_db_setup
):
    page.goto("/beispielstadt/mobilitat")

    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_should_go_to_subtask_view_when_clicking_task_item(page: Page, django_db_setup):
    page.goto("/beispielstadt/mobilitat")

    subtask_title = page.get_by_text("Radwege ausbauen")
    subtask_title.click()

    expect(page).to_have_url("/beispielstadt/verkehr/radwege-ausbauen/")
