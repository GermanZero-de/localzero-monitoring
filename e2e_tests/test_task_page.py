from playwright.sync_api import Page, expect


def test_the_task_page_should_have_the_city_name_in_the_title(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/massnahmen/mobilitat/")

    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_should_show_the_task_assessment(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/massnahmen/")

    expect(
        page.locator(
            ".card",
            has_text="Wie sieht es aus? Eine einleitende Übersicht in die Bewertung des Umsetzungsstandes. Hält die Kommune sich im Wesentlichen an ihren eigenen Plan?",
        )
    ).to_be_visible()


def test_should_go_to_subtask_view_when_clicking_task_item(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/massnahmen/mobilitat/")

    page.get_by_text("Radwege ausbauen").click()

    expect(page).to_have_url(
        live_server.url + "/beispielstadt/massnahmen/mobilitat/radwege-ausbauen/"
    )
