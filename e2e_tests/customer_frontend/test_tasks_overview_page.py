from playwright.sync_api import Page, expect


def test_the_task_overview_page_should_have_the_city_name_in_the_title(
    base_url: str, page: Page
):
    page.goto(f"{base_url}/beispielstadt/massnahmen")

    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_task_overview_page_should_show_the_city_logo(base_url: str, page: Page):
    logo_name = "Logo von Beispielstadt"

    page.goto(f"{base_url}/beispielstadt/massnahmen/")

    expect(page.get_by_role("img", name=logo_name)).to_be_visible()


def test_should_show_the_overall_assessment(base_url: str, page: Page):
    page.goto(f"{base_url}/beispielstadt/massnahmen")

    expect(
        page.locator(
            "p",
            has_text="Eine einleitende Übersicht in die Bewertung des Umsetzungsstandes. Hält die Kommune sich im Wesentlichen an ihren eigenen Plan?",
        )
    ).to_be_visible()
