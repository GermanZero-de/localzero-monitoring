from playwright.sync_api import Page, expect


def test_should_redirect_to_the_city_page_when_clicking_the_back_button(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/verwaltungsstrukturen_checkliste/")

    page.get_by_text("Zurück").click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/")
