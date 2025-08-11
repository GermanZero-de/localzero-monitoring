import pytest
from playwright.sync_api import Page, expect


def test_should_show_the_title_when_being_on_the_front_page(page: Page, base_url: str):
    page.goto(base_url)

    expect(page).to_have_title("LocalZero Monitoring")


def test_should_navigate_to_city_page_when_city_is_clicked(page: Page, base_url: str):
    page.goto(base_url)

    page.get_by_text("Beispielstadt").click()

    expect(page).to_have_url(f"{base_url}/beispielstadt")


def test_should_show_all_city_cards(page: Page, base_url: str):
    page.goto(base_url)

    city_tiles = page.get_by_test_id("city-tile")

    expect(city_tiles).to_have_count(3)
    expect(city_tiles).to_contain_text(["Beispielstadt", "Mitallem", "Ohnenix"])
