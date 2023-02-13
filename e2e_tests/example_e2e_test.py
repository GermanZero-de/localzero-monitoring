from playwright.sync_api import Page, expect


def test_should_show_the_title_when_being_on_the_front_page(page: Page):
    page.goto("/")

    expect(page).to_have_title("Klimaschutzmonitor")
