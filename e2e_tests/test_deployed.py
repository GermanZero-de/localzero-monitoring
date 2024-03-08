from playwright.sync_api import Page, expect


def test_should_provide_basic_website_functionality_when_using_the_deployed_application(
    page: Page,
):
    """
    This test requires starting the application with the local configuration and creating the database with migrations
    applied and `e2e_tests/database/test_database.json` loaded.
    """
    page.goto("https://localhost")

    page.locator(".card", has_text="Beispielstadt").click()

    expect(page).to_have_url("https://localhost/deutschland/beispielstadt/")
