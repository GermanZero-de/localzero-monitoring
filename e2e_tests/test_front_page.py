from playwright.sync_api import Page, expect


def test_should_show_the_title_when_being_on_the_front_page(
    django_db_setup, live_server, page: Page
):
    page.goto(live_server.url)

    expect(page).to_have_title("LocalZero Monitoring")


def test_should_show_the_city_name_in_city_select_dropdown(
    django_db_setup, live_server, page: Page
):
    page.goto(live_server.url)

    city_select_button = page.get_by_text("Stadt auswählen")
    city_select_button.click()

    assert "Beispielstadt" in page.get_by_role("listitem").all_inner_texts()
