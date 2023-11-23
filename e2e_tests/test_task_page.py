from playwright.sync_api import Page, expect


def test_the_task_page_should_have_the_city_name_in_the_title(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/massnahmen/mobilitat/")

    expect(page).to_have_title("LocalZero Monitoring - Beispielstadt")


def test_should_show_the_task_assessment(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/massnahmen/")

    expect(
        page.locator(
            "p",
            has_text="Eine einleitende Übersicht in die Bewertung des Umsetzungsstandes. Hält die Kommune sich im Wesentlichen an ihren eigenen Plan?",
        )
    ).to_be_visible()


def test_should_show_the_taskgroup_description(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/massnahmen/mobilitat/")
    expect(
        page.locator(
            "p",
            has_text="Die Maßnahmen in diesem Sektor dienen der Darstellung der verschiedenen Möglichkeiten.",
        )
    ).to_be_visible()


def test_should_go_to_subtask_view_when_clicking_task_item(live_server, page: Page):
    page.goto(live_server.url + "/beispielstadt/massnahmen/mobilitat/")

    page.get_by_text("Radwege ausbauen").click()

    expect(page).to_have_url(
        live_server.url + "/beispielstadt/massnahmen/mobilitat/radwege-ausbauen/"
    )


def test_should_go_to_the_linked_page_when_clicking_on_a_breadcrumb(
    live_server, page: Page
):
    page.goto(live_server.url + "/beispielstadt/massnahmen/mobilitat/radwege-ausbauen/")

    page.get_by_role("list", name="breadcrumbs").get_by_role(
        "link", name="Mobilität"
    ).click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/massnahmen/mobilitat/")

    page.get_by_role("list", name="breadcrumbs").get_by_role(
        "link", name="Maßnahmen"
    ).click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/massnahmen/")

    page.get_by_role("list", name="breadcrumbs").get_by_role(
        "link", name="Beispielstadt"
    ).click()

    expect(page).to_have_url(live_server.url + "/beispielstadt/")

    page.get_by_role("list", name="breadcrumbs").get_by_role(
        "link", name="Start"
    ).click()

    expect(page).to_have_url(live_server.url + "/")
