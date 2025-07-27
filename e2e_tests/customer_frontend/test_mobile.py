from playwright.sync_api import Page, expect


def test_can_see_burger_menu_in_mobile(live_server, page: Page):
    page.set_viewport_size({"width": 400, "height": 600})

    page.goto(live_server.url)
    menu = page.locator("#nav-burger")
    menu.click()
    expect(page.locator(".site-navigation")).to_be_visible()


def test_button_should_open_submenu(live_server, page: Page):
    page.set_viewport_size({"width": 400, "height": 600})

    page.goto(live_server.url)
    menu = page.locator("#nav-burger")
    menu.click()
    cities_button = page.get_by_role("button", name="Kommunen")
    cities_button.click()

    expect(page.locator(".show-sub-menu")).to_be_visible()
    expect(page.get_by_role("link", name="Beispielstadt", exact=True)).to_be_visible()
