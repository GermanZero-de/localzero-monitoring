import uuid
from playwright.sync_api import Page, expect
import pytest


@pytest.fixture
def admin_login(page: Page):
    page.goto("/admin")
    page.wait_for_selector("text=LocalZero Monitoring")
    page.fill("[name=username]", "admin")
    page.fill("[name=password]", "password")
    page.click("text=Anmelden")


def test_should_succeed_when_logging_into_admin(page: Page, admin_login):
    expect(page).to_have_title("Dateneingabe | LocalZero Monitoring")
    page.close()


def add_task(page, title, parent=None):
    page.goto("/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D1")
    page.fill("[name=title]", title)
    if parent:
        page.select_option("[name=_ref_node_id]", label=parent)
    page.click("[name=_save]")


def test_should_not_allow_duplicate_sectors(page: Page, admin_login):
    uid = str(uuid.uuid4())

    sector1 = "Admin Test " + uid + " 1"
    add_task(page, sector1)
    add_task(page, sector1)

    errlist = page.locator(".errorlist")
    expect(errlist.get_by_role("listitem")).to_contain_text(
        "Das kollidiert mit einem anderen Eintrag."
    )

    page.close()


def test_should_allow_add_when_same_title_in_another_sector(page: Page, admin_login):
    uid = str(uuid.uuid4())

    sector1 = "Admin Test " + uid + " 1"
    add_task(page, sector1)
    add_task(page, "Personal Einstellen", sector1)

    sector2 = "Admin Test " + uid + " 2"
    add_task(page, sector2)
    add_task(page, "Personal Einstellen", sector2)

    msglist = page.locator(".messagelist")
    expect(msglist).to_contain_text(
        "„Personal Einstellen“ wurde erfolgreich hinzugefügt."
    )

    page.close()


def test_should_not_allow_add_when_same_title_in_same_sector(page: Page, admin_login):
    uid = str(uuid.uuid4())

    sector1 = "Admin Test " + uid + " 1"
    add_task(page, sector1)
    add_task(page, "Personal Einstellen", sector1)
    add_task(page, "personal einstellen", sector1)

    errlist = page.locator(".errorlist")
    expect(errlist.get_by_role("listitem")).to_contain_text(
        "Das kollidiert mit einem anderen Eintrag."
    )

    page.close()
