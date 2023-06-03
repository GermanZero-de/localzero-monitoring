from playwright.sync_api import Page, expect


def test_should_show_the_title_when_being_on_the_front_page(live_server, page: Page):
    page.goto(live_server.url)

    expect(page).to_have_title("LocalZero Monitoring")


def test_should_show_the_city_name_in_city_select_dropdown(live_server, page: Page):
    page.goto(live_server.url)

    city_select_button = page.get_by_text("Stadt auswählen")
    city_select_button.click()

    assert "Beispielstadt" in page.get_by_role("listitem").all_inner_texts()


def test_should_show_the_city_cards_with_an_introductory_text(live_server, page: Page):
    page.goto(live_server.url)

    city_card1 = page.locator(".card", has_text="Beispielstadt")
    city_card2 = page.locator(".card", has_text="Ohnenix")
    city_card3 = page.locator(".card", has_text="Mitallem")

    expect(city_card1).to_contain_text(
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been…"
    )
    expect(city_card2).to_contain_text(
        "Eine Kommune ohne jegliche Infos. Muss ja auch getestet werden."
    )
    expect(city_card3).to_contain_text("Diese Kommune hat gaaanz viele Daten.")


def test_should_show_go_to_the_respective_city_page_when_clicking_on_a_city_card(
    live_server, page: Page
):
    page.goto(live_server.url)

    page.locator(".card", has_text="Beispielstadt").click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/")
