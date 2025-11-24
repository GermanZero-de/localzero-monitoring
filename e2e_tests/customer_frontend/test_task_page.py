from playwright.sync_api import Page, expect
import pytest


@pytest.fixture
def page(base_url: str, page: Page):
    page.goto(f"{base_url}/beispielstadt/massnahmen/mobilitat/radwege-ausbauen")
    return page


def test_the_task_page_should_have_the_city_name_in_the_title(page: Page):
    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_task_page_should_show_the_city_logo(base_url: str, page: Page):
    logo_name = "Logo von Beispielstadt"
    page.goto(
        f"{base_url}/beispielstadt/massnahmen/mobilitat/u-bahn-strecke-verlangern/"
    )
    expect(page.get_by_role("img", name=logo_name)).to_be_visible()


def test_should_show_the_task_assessment(page: Page):
    expect(
        page.get_by_text("Radspuren mit einer Mindestbreite von 2,30 Metern")
    ).to_be_visible()


def test_should_show_the_plan_assessment(page: Page):
    expect(
        page.get_by_role("heading", name="Bewertung der geplanten Maßnahme")
    ).to_be_visible()
    expect(
        page.get_by_text("Bisher sind 12% der geplanten Radwege gebaut.")
    ).to_be_visible()


def test_should_show_the_execution_justification(page: Page):
    expect(
        page.get_by_role("heading", name="Begründung Umsetzungsstand")
    ).to_be_visible()
    expect(
        page.get_by_text(
            "Straßen werden nur umgebaut, wenn auch andere bauliche Maßnahmen geplant sind."
        )
    ).to_be_visible()


def test_should_show_the_responsible_organ_explanation(page: Page):
    expect(page.get_by_role("heading", name="Zuständige Instanz")).to_be_visible()
    expect(
        page.get_by_text("Anschrift Baureferat Landeshauptstadt Beispielstadt")
    ).to_be_visible()


def test_should_go_to_the_linked_page_when_clicking_on_a_breadcrumb(
    base_url: str, page: Page
):
    page.get_by_role("link", name="Mobilität").click()

    expect(page).to_have_url(f"{base_url}/beispielstadt/massnahmen/mobilitat")

    page.get_by_role("link", name="Maßnahmen").click()

    expect(page).to_have_url(f"{base_url}/beispielstadt/massnahmen")

    page.get_by_role("link", name="Dashboard").click()

    expect(page).to_have_url(f"{base_url}/beispielstadt")


def test_task_page_should_display_parent_task_group_in_sidebar(page: Page):
    # search for joined text of two adjacent divs
    expect(page.get_by_text("Sektor:Mobilität")).to_be_visible()


def test_task_page_should_display_begin_date_in_sidebar(page: Page):
    # search for joined text of two adjacent divs
    expect(page.get_by_text("Beginn:4.11.2024")).to_be_visible()


def test_task_page_should_display_end_date_in_sidebar(page: Page):
    # search for joined text of two adjacent divs
    expect(page.get_by_text("Ende:28.11.2099")).to_be_visible()


def test_task_page_should_display_responsible_organ_in_sidebar(page: Page):
    # search for joined text of two adjacent divs
    expect(page.get_by_text("Zuständigkeit:Baureferat")).to_be_visible()


@pytest.fixture
def task_suggested_by_ngo_page(base_url: str, page: Page):
    page.goto(
        f"{base_url}/beispielstadt/massnahmen/umstellung-fernwarme-auf-geothermie"
    )
    return page


def test_task_page_should_display_supporting_ngos_in_sidebar(
    task_suggested_by_ngo_page: Page,
):
    expect(task_suggested_by_ngo_page.get_by_text("Kooperation:")).to_be_visible()
    expect(
        task_suggested_by_ngo_page.get_by_role("link", name="aidfive")
    ).to_be_visible()
