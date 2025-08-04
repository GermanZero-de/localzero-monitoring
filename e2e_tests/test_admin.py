from django.utils.text import slugify
from playwright.sync_api import Page, expect


def admin_login(base_url: str, page: Page):
    page.goto(base_url + "/admin/")
    page.wait_for_selector("text=LocalZero Monitoring")
    page.locator("#id_username").fill("admin")
    page.locator("#id_password").fill("password")
    page.get_by_text("Anmelden").click()


def go_to_cap_edit_board(page: Page, city: str):
    page.get_by_text("KAP editieren").click()
    page.get_by_text(city).click()


def add_task(base_url: str, page: Page, title, parent=None):
    page.goto(
        base_url + "/admin/cpmonitor/task/add/?_changelist_filters=city__id__exact%3D1"
    )
    page.fill("[name=title]", title)
    if parent:
        full_parent = page.get_by_text(parent).all_inner_texts()[0]
        page.get_by_label("relativ zu").select_option(label=full_parent)
    page.get_by_role("button", name="Sichern", exact=True).first.click()


def drag_task_on_task_on_the_cap_board(
    page: Page, task_to_drag_title: str, target_task_title: str
):
    task_to_drag = page.get_by_text(task_to_drag_title)
    target_task = page.locator(".cap_board__task-item", has_text=target_task_title)
    target_task.scroll_into_view_if_needed()

    to_drag_x, to_drag_y = get_position_in_the_middle(task_to_drag)
    target_x, target_y = get_position_in_the_lower_third(target_task)

    page.mouse.move(to_drag_x, to_drag_y)
    page.mouse.down()
    page.mouse.move(target_x, target_y)
    page.mouse.up()


def drag_task_above_task_on_the_cap_board(
    page: Page, task_to_drag_title: str, target_task_title: str
):
    task_to_drag = page.get_by_text(task_to_drag_title)
    target_task = page.locator(".cap_board__task-item", has_text=target_task_title)
    target_task.scroll_into_view_if_needed()

    to_drag_x, to_drag_y = get_position_in_the_middle(task_to_drag)
    target_x, target_y = get_position_in_the_upper_third(target_task)

    page.mouse.move(to_drag_x, to_drag_y)
    page.mouse.down()
    page.mouse.move(target_x, target_y)
    page.mouse.up()


def drag_task(page: Page, task_to_drag: str, target_task: str):
    target_locator = page.get_by_role("link", name=target_task)

    drag_handler = page.locator(
        f"//th[@class='field-title' and contains(., '{task_to_drag}')]/preceding-sibling::td[@class='drag-handler']/span"
    )
    target_locator.scroll_into_view_if_needed()

    to_drag_x, to_drag_y = get_position_in_the_middle(drag_handler)
    target_x, target_y = get_position_in_the_lower_third(target_locator)

    page.mouse.move(to_drag_x, to_drag_y)
    page.mouse.down()
    page.mouse.move(target_x, target_y)
    page.mouse.up()


def get_position_in_the_middle(drag_handler):
    drag_handler_bounding_box = drag_handler.bounding_box()
    to_drag_x = drag_handler_bounding_box["x"] + drag_handler_bounding_box["width"] / 2
    to_drag_y = drag_handler_bounding_box["y"] + drag_handler_bounding_box["height"] / 2
    return to_drag_x, to_drag_y


def get_position_in_the_lower_third(target_locator):
    target_bounding_box = target_locator.bounding_box()
    target_x = target_bounding_box["x"] + target_bounding_box["width"] / 2
    target_y = target_bounding_box["y"] + target_bounding_box["height"] * 2 / 3
    return target_x, target_y


def get_position_in_the_upper_third(target_locator):
    target_bounding_box = target_locator.bounding_box()
    target_x = target_bounding_box["x"] + target_bounding_box["width"] / 2
    target_y = target_bounding_box["y"] + target_bounding_box["height"] * 1 / 3
    return target_x, target_y


def test_should_succeed_when_logging_into_admin(live_server, page: Page):
    admin_login(live_server.url, page)
    expect(page).to_have_title("Dateneingabe | LocalZero Monitoring")


def test_should_not_allow_duplicate_sectors(live_server, page: Page):
    admin_login(live_server.url, page)

    sector1 = "Handlungsfeld 1"
    add_task(live_server.url, page, sector1)
    add_task(live_server.url, page, sector1)

    errlist = page.locator(".errorlist")
    expect(errlist.get_by_role("listitem")).to_contain_text(
        "Das kollidiert mit einem anderen Eintrag."
    )


def test_should_allow_add_when_same_title_in_another_sector(live_server, page: Page):
    admin_login(live_server.url, page)

    sector1 = "Handlungsfeld 1"
    add_task(live_server.url, page, sector1)
    add_task(live_server.url, page, "Personal Einstellen", sector1)

    sector2 = "Handlungsfeld 2"
    add_task(live_server.url, page, sector2)
    add_task(live_server.url, page, "Personal Einstellen", sector2)

    msglist = page.locator(".messagelist")
    expect(msglist).to_contain_text(
        "„Personal Einstellen“ wurde erfolgreich hinzugefügt."
    )


def test_should_not_allow_add_when_same_title_in_same_sector(live_server, page: Page):
    admin_login(live_server.url, page)

    sector1 = "Handlungsfeld 1"
    add_task(live_server.url, page, sector1)
    add_task(live_server.url, page, "Personal Einstellen", sector1)
    add_task(live_server.url, page, "personal einstellen", sector1)

    errlist = page.locator(".errorlist")
    expect(errlist.get_by_role("listitem")).to_contain_text(
        "Das kollidiert mit einem anderen Eintrag."
    )


def test_should_also_move_subtasks_when_dragging_a_task_with_subtasks_to_a_different_sektor(
    live_server, page: Page
):
    admin_login(live_server.url, page)

    sector1 = "Handlungsfeld 1"
    sector2 = "Handlungsfeld 2"
    task = "To be dragged"
    sub_task = "Subtask"
    sub_sub_task = "Subsubtask"

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

    page.goto(live_server.url + "/admin/cpmonitor/task/?all=&city__id__exact=1")

    expect(page.get_by_text(slug_s1 + "/" + slugify(task), exact=True)).to_be_visible()
    expect(page.get_by_text(slug_s2 + "/" + slugify(task))).not_to_be_visible()
    expect(page.get_by_text(slug_s1 + sub_sub_slug)).to_be_visible()
    expect(page.get_by_text(slug_s2 + sub_sub_slug)).not_to_be_visible()

    drag_task(page, task, sector2)

    expect(page.locator(".messagelist")).to_contain_text("positioniert unterhalb von")

    expect(page.get_by_text(slug_s1 + "/" + slugify(task))).not_to_be_visible()
    expect(page.get_by_text(slug_s2 + "/" + slugify(task), exact=True)).to_be_visible()
    expect(page.get_by_text(slug_s1 + sub_sub_slug)).not_to_be_visible()
    expect(page.get_by_text(slug_s2 + sub_sub_slug)).to_be_visible()


# Fixme: #350
# def test_should_not_allow_to_move_a_task_to_a_sector_which_contains_a_task_with_the_same_title_ignoring_the_case(
#     live_server, page: Page
# ):
#     admin_login(live_server.url, page)
#
#     sector1 = "Handlungsfeld 1"
#     sector2 = "Handlungsfeld 2"
#     task1 = "Same Task Title"
#     task2 = task1.lower()
#
#     add_task(live_server.url, page, sector1)
#     add_task(live_server.url, page, task1, sector1)
#     add_task(live_server.url, page, sector2)
#     add_task(live_server.url, page, task2, sector2)
#
#     page.goto(live_server.url + "/admin/cpmonitor/task/?all=&city__id__exact=1")
#
#     drag_task(page, task1, sector2)
#
#     expect(page.locator(".messagelist")).to_contain_text(
#         "Es gibt bereits ein Handlungsfeld / eine Maßnahme mit der URL"
#     )


def test_should_allow_local_groups_without_image(live_server, page: Page):
    admin_login(live_server.url, page)
    page.get_by_role("link", name="Kommunen").click()
    page.get_by_role("link", name="Ohnenix").click()

    page.locator("#id_local_group-0-name").fill("OhnenixZero")
    page.get_by_role("button", name="Sichern", exact=True).first.click()
    expect(page.get_by_text("erfolgreich geändert")).to_be_visible()


def test_should_add_the_task_to_the_chosen_sector_when_clicking_add_new_task(
    live_server, page: Page
):
    # given
    sector_id = "#column-7"
    new_task_title = "Maßnahme 1"

    # when
    admin_login(live_server.url, page)
    go_to_cap_edit_board(page, "Beispielstadt")
    page.locator(sector_id).get_by_role("link", name="Neue Maßnahme hinzufügen").click()

    page.fill("[name=title]", new_task_title)
    page.get_by_role("button", name="Sichern", exact=True).first.click()

    # then
    go_to_cap_edit_board(page, "Beispielstadt")
    column = page.locator(sector_id)
    new_task = column.get_by_text(new_task_title)
    expect(new_task).to_be_visible()


def test_should_delete_the_task_when_clicking_on_the_delete_button(
    live_server, page: Page
):
    # given
    task_title = "Klimaaktionsplan"

    # when
    admin_login(live_server.url, page)
    go_to_cap_edit_board(page, "Beispielstadt")
    page.locator(".cap_board__task-item", has_text=task_title).get_by_text(
        "Löschen"
    ).click()
    page.get_by_text("Ja, ich bin sicher").click()

    # then
    go_to_cap_edit_board(page, "Beispielstadt")
    expect(page.get_by_text(task_title)).not_to_be_visible()


def test_should_move_the_task_to_the_top_level_of_the_chosen_sector_when_moving_a_task_above_another_task(
    live_server, page: Page
):
    # given
    sector_id = "#column-7"
    task_title = "Jobtickets für Verwaltung"
    target_task_title = "Klimaaktionsplan"

    # when
    admin_login(live_server.url, page)
    go_to_cap_edit_board(page, "Beispielstadt")
    drag_task_above_task_on_the_cap_board(page, task_title, target_task_title)

    # then
    column = page.locator(sector_id)
    dragged_task = column.locator(".cap_board__task-item", has_text=task_title)
    expect(dragged_task).to_be_visible()
    expect(dragged_task.locator("//parent::div").get_by_role("img")).to_have_class(
        "inline marginleft-0"
    )


def test_should_move_the_task_below_the_chosen_task_when_moving_a_task_on_another_task(
    live_server, page: Page
):
    # given
    sector_id = "#column-7"
    task_title = "Jobtickets für Verwaltung"
    target_task_title = "Klimaaktionsplan"

    # when
    admin_login(live_server.url, page)
    go_to_cap_edit_board(page, "Beispielstadt")
    drag_task_on_task_on_the_cap_board(page, task_title, target_task_title)

    # then
    column = page.locator(sector_id)
    dragged_task = column.locator(".cap_board__task-item", has_text=task_title)
    expect(dragged_task).to_be_visible()
    expect(dragged_task.locator("//parent::div").get_by_role("img")).to_have_class(
        "inline marginleft-1"
    )


def test_should_add_cap_checklist_to_the_respective_city_when_clicking_add_new_cap_checklist(
    live_server, page: Page
):
    # when
    admin_login(live_server.url, page)
    go_to_cap_edit_board(page, "Ohnenix")
    page.get_by_text("Checkliste zum KAP").get_by_role(
        "link", name="hinzufügen"
    ).click()

    # then
    expect(page.get_by_label("Stadt")).to_contain_text("Ohnenix")
    page.get_by_label("Gibt es einen Klima-Aktionsplan").check()
    page.get_by_role("button", name="Sichern", exact=True).first.click()


def test_should_add_administration_checklist_to_the_respective_city_when_clicking_add_new_administration_checklist(
    live_server, page: Page
):
    # when
    admin_login(live_server.url, page)
    go_to_cap_edit_board(page, "Ohnenix")
    page.get_by_text("Checkliste zu Verwaltungsstrukturen").get_by_role(
        "link", name="hinzufügen"
    ).click()

    # then
    expect(page.get_by_label("Stadt")).to_contain_text("Ohnenix")
    page.get_by_label("Gibt es ein Klimaschutzmanagement").check()
    page.get_by_role("button", name="Sichern", exact=True).first.click()


def test_should_add_heat_plan_checklist_to_the_respective_city_when_clicking_add_new_heat_plan_checklist(
    live_server, page: Page
):
    # when
    admin_login(live_server.url, page)
    go_to_cap_edit_board(page, "Ohnenix")
    page.get_by_text("Checkliste zur Wärmeplanung").get_by_role(
        "link", name="hinzufügen"
    ).click()

    # then
    expect(page.get_by_label("Stadt")).to_contain_text("Ohnenix")
    page.get_by_label(
        "Liegt ein öffentlich bekannt gemachter Beschluss zur Durchführung der Wärmeplanung vor?"
    ).check()
    page.get_by_role("button", name="Sichern", exact=True).first.click()


def test_should_show_the_checkist_add_button_when_a_checklist_was_deleted(
    live_server, page: Page
):
    # when
    admin_login(live_server.url, page)
    go_to_cap_edit_board(page, "Beispielstadt")
    page.get_by_text("Checkliste zum KAP").get_by_role("link", name="löschen").click()
    page.get_by_text("Ja, ich bin sicher").click()

    # then
    go_to_cap_edit_board(page, "Beispielstadt")
    expect(
        page.get_by_text("Checkliste zum KAP").get_by_role("link", name="löschen")
    ).not_to_be_visible()
    expect(
        page.get_by_text("Checkliste zum KAP").get_by_role("link", name="editieren")
    ).not_to_be_visible()
    expect(
        page.get_by_text("Checkliste zum KAP").get_by_role("link", name="hinzufügen")
    ).to_be_visible()
