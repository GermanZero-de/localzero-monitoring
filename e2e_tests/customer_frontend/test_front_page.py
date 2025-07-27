import re

from playwright.sync_api import Page, expect


def test_should_show_the_title_when_being_on_the_front_page(live_server, page: Page):
    page.goto(live_server.url)

    expect(page).to_have_title("LocalZero Monitoring")


def test_should_show_the_city_name_in_city_select_dropdown(live_server, page: Page):
    page.goto(live_server.url)

    city_select_button = page.get_by_role("button", name="Kommunen")
    city_select_button.click()

    city_link = page.get_by_role("link", name="Beispielstadt", exact=True)
    expect(city_link).to_contain_text("Beispielstadt")


def test_should_show_the_city_cards_with_an_introductory_text(live_server, page: Page):
    page.goto(live_server.url)

    city_card1 = page.locator(".card", has_text="Beispielstadt")
    city_card2 = page.locator(".card", has_text="Ohnenix")
    city_card3 = page.locator(".card", has_text="Mitallem")

    expect(city_card1).to_contain_text(
        re.compile(
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been t"
        )
    )
    expect(city_card2).to_contain_text(
        re.compile("Eine Kommune ohne jegliche Infos. Muss ja auch getestet werden.")
    )
    expect(city_card3).to_contain_text(
        re.compile("Diese Kommune hat gaaanz viele Daten.")
    )


def test_should_show_go_to_the_respective_city_page_when_clicking_on_a_city_card(
    live_server, page: Page
):
    page.goto(live_server.url)

    page.locator(".card", has_text="Beispielstadt").click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/")
