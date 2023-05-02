import uuid

from django.utils.text import slugify
from playwright.sync_api import Page, expect


def admin_login(base_url: str, page: Page):
    page.goto(base_url + "/admin/")
    page.wait_for_selector("text=LocalZero Monitoring")
    page.locator("#id_username").fill("admin")
    page.locator("#id_password").fill("password")
    page.get_by_role("button").click()


def add_task(base_url: str, page: Page, title, parent=None):
    page.goto(
        base_url + "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D1"
    )
    page.fill("[name=title]", title)
    if parent:
        full_parent = page.get_by_text(parent).all_inner_texts()[0]
        page.get_by_label("relativ zu").select_option(label=full_parent)
    page.click("[name=_save]")


def drag_task_to(page, dragged_task, target_task):
    target_locator = page.locator(
        f"//*[@class='field-title' and contains(., '{target_task}')]"
    )

    drag_handler = page.locator(
        f"//th[@class='field-title' and contains(., '{dragged_task}')]/preceding-sibling::td[@class='drag-handler']/span"
    )

    drag_handler.drag_to(
        target_locator,
        target_position={"x": 10, "y": 50},
        force=True,
        timeout=1000,
    )


def test_should_succeed_when_logging_into_admin(live_server, page: Page):
    page.goto(live_server.url + "/admin/")
    page.wait_for_selector("text=LocalZero Monitoring")
    page.locator("#id_username").fill("admin")
    page.locator("#id_password").fill("password")
    page.get_by_role("button").click()
    expect(page).to_have_title("Dateneingabe | LocalZero Monitoring")
    page.close()


def test_should_not_allow_duplicate_sectors(live_server, page: Page):
    admin_login(live_server.url, page)

    uid = str(uuid.uuid4())

    sector1 = "Admin Test " + uid + " 1"
    add_task(live_server.url, page, sector1)
    add_task(live_server.url, page, sector1)

    errlist = page.locator(".errorlist")
    expect(errlist.get_by_role("listitem")).to_contain_text(
        "Das kollidiert mit einem anderen Eintrag."
    )

    page.close()


def test_should_allow_add_when_same_title_in_another_sector(live_server, page: Page):
    admin_login(live_server.url, page)
    uid = str(uuid.uuid4())

    sector1 = "Admin Test " + uid + " 1"
    page.goto(
        live_server.url
        + "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D1"
    )
    add_task(live_server.url, page, sector1)
    add_task(live_server.url, page, "Personal Einstellen", sector1)

    sector2 = "Admin Test " + uid + " 2"
    add_task(live_server.url, page, sector2)
    add_task(live_server.url, page, "Personal Einstellen", sector2)

    msglist = page.locator(".messagelist")
    expect(msglist).to_contain_text(
        "„Personal Einstellen“ wurde erfolgreich hinzugefügt."
    )

    page.close()


def test_should_not_allow_add_when_same_title_in_same_sector(live_server, page: Page):
    admin_login(live_server.url, page)
    uid = str(uuid.uuid4())

    sector1 = "Admin Test " + uid + " 1"
    page.goto(
        live_server.url
        + "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D1"
    )
    add_task(live_server.url, page, sector1)
    add_task(live_server.url, page, "Personal Einstellen", sector1)
    add_task(live_server.url, page, "personal einstellen", sector1)

    errlist = page.locator(".errorlist")
    expect(errlist.get_by_role("listitem")).to_contain_text(
        "Das kollidiert mit einem anderen Eintrag."
    )

    page.close()


def test_should_move_and_adjust_slugs_when_dragged(live_server, page: Page):
    admin_login(live_server.url, page)
    uid = str(uuid.uuid4())

    sector1 = "Admin Test 1 " + uid
    sector2 = "Admin Test 2 " + uid
    task = "To be dragged " + uid
    sub_task = "Has to be adjusted " + uid
    sub_sub_task = "Has to be adjusted " + uid

    slug_s1 = slugify(sector1)
    slug_s2 = slugify(sector2)
    sub_sub_slug = (
        "/" + slugify(task) + "/" + slugify(sub_task) + "/" + slugify(sub_sub_task)
    )

    add_task(live_server.url, page, sector1)
    add_task(live_server.url, page, task, sector1)
    add_task(live_server.url, page, sub_task, task)
    add_task(live_server.url, page, sub_sub_task, sub_task)

    add_task(live_server.url, page, sector2)

    # Make sure, all are visible and not hidden on page 2.
    page.goto(live_server.url + "/admin/cpmonitor/task/?all=&city__id__exact=1")

    # Without exact=True this would also catch the sub-tasks:
    expect(page.get_by_text(slug_s1 + "/" + slugify(task), exact=True)).to_be_visible()
    # ...on the other hand, this should catch any sub-tasks:
    expect(page.get_by_text(slug_s2 + "/" + slugify(task))).not_to_be_visible()
    expect(page.get_by_text(slug_s1 + sub_sub_slug)).to_be_visible()
    expect(page.get_by_text(slug_s2 + sub_sub_slug)).not_to_be_visible()

    drag_task_to(page, task, sector2)

    expect(page.locator(".messagelist")).to_contain_text("positioniert unterhalb von")

    expect(page.get_by_text(slug_s1 + "/" + slugify(task))).not_to_be_visible()
    expect(page.get_by_text(slug_s2 + "/" + slugify(task), exact=True)).to_be_visible()
    expect(page.get_by_text(slug_s1 + sub_sub_slug)).not_to_be_visible()
    expect(page.get_by_text(slug_s2 + sub_sub_slug)).to_be_visible()

    page.close()


def test_should_not_allow_move_when_same_case_ignored_title_in_same_sector(
    live_server, page: Page
):
    admin_login(live_server.url, page)
    uid = str(uuid.uuid4())

    sector1 = "Admin Test 1 " + uid
    sector2 = "Admin Test 2 " + uid
    task1 = "Personal Einstellen " + uid
    task2 = "personal einstellen " + uid

    add_task(live_server.url, page, sector1)
    add_task(live_server.url, page, task1, sector1)

    add_task(live_server.url, page, sector2)
    add_task(live_server.url, page, task2, sector2)

    # Make sure all tasks are visible
    page.goto(live_server.url + "/admin/cpmonitor/task/?all=&city__id__exact=1")

    drag_task_to(page, task2, sector1)

    expect(page.locator(".messagelist")).to_contain_text(
        "Es gibt bereits einen Sektor / eine Maßnahme mit der URL "
    )

    page.close()
