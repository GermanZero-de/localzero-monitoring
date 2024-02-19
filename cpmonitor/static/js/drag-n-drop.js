$(document).ready(function () {
  $(".cap_board__task-item")
    .on("dragstart", function (ev) {
      onDragStart(ev);
    })
    .on("dragover", function (ev) {
      onDragOver(ev);
    })
    .on("dragleave", function (ev) {
      onDragLeave(ev);
    })
    .on("drop", function (ev) {
      dropLeftOf(ev, this);
    });

  // $(".cap_board__task-area")
  //   .on("dragover", function (ev) {
  //     allowDrop(ev);
  //   })
  //   .on("drop", function (ev) {
  //     dropOnColumn(ev, this);
  //   });

  function onDragOver(ev) {
    ev.preventDefault();
    const targetTaskId = ev.currentTarget.id;
    const target = document.getElementById(targetTaskId);
    target.classList.add("drag-over");
  }

  function onDragLeave(ev) {
    ev.preventDefault();
    const targetTaskId = ev.currentTarget.id;
    const target = document.getElementById(targetTaskId);
    target.classList.remove("drag-over");
  }

  function onDragStart(ev) {
    ev.originalEvent.dataTransfer.setData("text", ev.currentTarget.id);
  }

  function dropLeftOf(ev) {
    ev.preventDefault();
    const task_id = ev.originalEvent.dataTransfer.getData("text");
    const new_parent_id = ev.currentTarget.id;

    const task_pk = task_id.split("-")[1];
    const new_parent_pk = new_parent_id.split("-")[1];

    moveTask(task_pk, new_parent_pk, "left");
  }

  function dropOnColumn(ev) {
    ev.preventDefault();
    const task_id = ev.originalEvent.dataTransfer.getData("text");
    const column_id = ev.currentTarget.id;

    const task_pk = task_id.split("-")[1];
    const column_pk = column_id.split("-")[1];

    moveTask(task_pk, column_pk, "last-child");
  }

  function moveTask(task_pk, new_parent_pk, position) {
    const csrftoken = document.querySelector(
      "[name=csrfmiddlewaretoken]",
    ).value;

    $.ajax({
      url: "/admin/cap/task/move/" + task_pk + "/",
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      mode: "same-origin", // do not send the CSRF token to another domain
      data: { new_parent_pk: new_parent_pk, position: position },
    }).done(function (data) {
      location.reload();
    });
  }
});
