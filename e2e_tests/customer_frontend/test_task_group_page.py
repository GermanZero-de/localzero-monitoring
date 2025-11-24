import re
from playwright.sync_api import Page, expect


def test_the_task_group_page_should_have_the_city_name_in_the_title(
    base_url: str, page: Page
):
    page.goto(f"{base_url}/beispielstadt/massnahmen/mobilitat")

    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_task_group_page_should_show_the_city_logo(base_url: str, page: Page):
    logo_name = "Logo von Beispielstadt"

    page.goto(f"{base_url}/beispielstadt/massnahmen/mobilitat/")

    expect(page.get_by_role("img", name=logo_name)).to_be_visible()


def test_should_show_the_taskgroup_teaser(base_url: str, page: Page):
    page.goto(f"{base_url}/beispielstadt/massnahmen/mobilitat/")
    expect(
        page.locator(
            "p",
            has_text="Auch in der Mobilität muss sich einiges ändern.",
        )
    ).to_be_visible()


def test_should_show_the_taskgroup_description(base_url: str, page: Page):
    page.goto(f"{base_url}/beispielstadt/massnahmen/mobilitat/")
    expect(
        page.locator(
            "p",
            has_text="Die Maßnahmen in diesem Handlungsfeld dienen der Darstellung der verschiedenen Möglichkeiten.",
        )
    ).to_be_visible()


def test_should_go_to_task_overview_when_clicking_back_button(
    base_url: str, page: Page
):
    page.goto(f"{base_url}/beispielstadt/massnahmen/mobilitat/")

    page.get_by_role("link", name="zurück").click()

    expect(page).to_have_url(
        # ignore URL parameters
        re.compile(re.escape(base_url) + r"/beispielstadt/massnahmen(\?.*)?")
    )
