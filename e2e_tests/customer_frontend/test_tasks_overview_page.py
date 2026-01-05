import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def page(page: Page, base_url: str) -> Page:
    """Starts at tasks overview page."""
    page.goto(f"{base_url}/beispielstadt/massnahmen")
    return page


def test_the_task_overview_page_should_have_the_city_name_in_the_title(page: Page):
    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_task_overview_page_should_show_the_city_logo(page: Page):
    expect(page.get_by_role("img", name="Logo von Beispielstadt")).to_be_visible()


def test_should_show_the_overall_assessment(page: Page):
    expect(
        page.locator(
            "p",
            has_text="Eine einleitende Übersicht in die Bewertung des Umsetzungsstandes. Hält die Kommune sich im Wesentlichen an ihren eigenen Plan?",
        )
    ).to_be_visible()


def test_should_show_the_start_and_end_dates(page: Page):
    expect(page.get_by_text("2021")).to_be_visible()
    expect(page.get_by_text("2035")).to_be_visible()


def test_should_show_published_top_level_sector(page: Page):
    expect(page.get_by_role("heading", name="Mobilität")).to_be_visible()


def test_should_show_published_nested_task(page: Page):
    page.get_by_role("heading", name="Mobilität").click()
    expect(page.get_by_text("U-Bahn Strecke verlängern")).to_be_visible()


def test_should_not_show_draft_top_level_sector(page: Page):
    """We can only test the absence of top level tasks, since nested elements will never be shown when the parent isn't visible."""
    expect(page.get_by_role("heading", name="Strukturen")).not_to_be_visible()
