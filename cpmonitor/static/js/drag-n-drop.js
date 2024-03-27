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
      drop(ev, this);
    });

  $(".column-drop-area")
    .on("dragover", function (ev) {
      onDragOverColumnDropArea(ev);
    })
    .on("dragleave", function (ev) {
      onDragLeaveColumnDropArea(ev);
    })
    .on("drop", function (ev) {
      drop(ev, this);
    });

  function onDragOver(ev) {
    ev.preventDefault();
    const targetTaskId = ev.currentTarget.id;
    const target = document.getElementById(targetTaskId);

    if (isUpperHalf(event.clientY, target)) {
      target.classList.add("drag-over-top");
      target.classList.remove("drag-over-middle");
    } else {
      target.classList.add("drag-over-middle");
      target.classList.remove("drag-over-top");
    }
  }

  function onDragOverColumnDropArea(ev) {
    ev.preventDefault();
    const columnDropAreaClass = ev.currentTarget.id;
    const target = document.getElementById(columnDropAreaClass);
    target.classList.add("drag-over-middle");
  }

  function isUpperHalf(mouseY, target) {
    const targetRect = target.getBoundingClientRect();
    const targetTop = targetRect.top;
    const targetHeight = targetRect.height;

    return mouseY < targetTop + targetHeight / 2;
  }

  function onDragLeave(ev) {
    ev.preventDefault();
    const targetTaskId = ev.currentTarget.id;
    const target = document.getElementById(targetTaskId);
    target.classList.remove("drag-over-top", "drag-over-middle");
  }

  function onDragLeaveColumnDropArea(ev) {
    ev.preventDefault();
    const columnDropAreaClass = ev.currentTarget.id;
    const target = document.getElementById(columnDropAreaClass);
    target.classList.remove("drag-over-middle");
  }

  function onDragStart(ev) {
    ev.originalEvent.dataTransfer.setData("text", ev.currentTarget.id);
  }

  function drop(ev) {
    ev.preventDefault();
    const task_id = ev.originalEvent.dataTransfer.getData("text");
    const new_parent_id = ev.currentTarget.id;

    const task_pk = task_id.split("-")[1];
    const new_parent_pk = new_parent_id.split("-")[1];

    const target = document.getElementById(new_parent_id);
    if (target.classList.contains("drag-over-top")) {
      moveTask(task_pk, new_parent_pk, "left");
    }
    if (target.classList.contains("drag-over-middle")) {
      moveTask(task_pk, new_parent_pk, "last-child");
    }
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
