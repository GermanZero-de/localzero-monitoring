$(document).ready(function () {
  $(".cap_board__task-item")
    .on("dragstart", function (event) {
      onDragStart(event);
    })
    .on("dragover", function (event) {
      onDragOver(event);
    })
    .on("dragleave", function (event) {
      onDragLeave(event);
    })
    .on("drop", function (event) {
      drop(event, this);
    });

  $(".dropping-area")
    .on("dragover", function (event) {
      onDragOverDroppingArea(event);
    })
    .on("dragleave", function (event) {
      onDragLeaveDroppingArea(event);
    })
    .on("drop", function (event) {
      drop(event, this);
    });

  function onDragOver(event) {
    event.preventDefault();
    const targetTaskId = event.currentTarget.id;
    const target = document.getElementById(targetTaskId);

    if (isUpperHalf(event.clientY, target)) {
      target.classList.add("drag-over-top");
      target.classList.remove("drag-over-middle");
    } else {
      target.classList.add("drag-over-middle");
      target.classList.remove("drag-over-top");
    }
  }

  function onDragOverDroppingArea(event) {
    event.preventDefault();
    const droppingAreaClass = event.currentTarget.id;
    const target = document.getElementById(droppingAreaClass);
    target.classList.add("drag-over-middle");
  }

  function isUpperHalf(mouseY, target) {
    const targetRect = target.getBoundingClientRect();
    const targetTop = targetRect.top;
    const targetHeight = targetRect.height;

    return mouseY < targetTop + targetHeight / 2;
  }

  function onDragLeave(event) {
    event.preventDefault();
    const targetTaskId = event.currentTarget.id;
    const target = document.getElementById(targetTaskId);
    target.classList.remove("drag-over-top", "drag-over-middle");
  }

  function onDragLeaveDroppingArea(event) {
    event.preventDefault();
    const droppingAreaClass = event.currentTarget.id;
    const target = document.getElementById(droppingAreaClass);
    target.classList.remove("drag-over-middle");
  }

  function onDragStart(event) {
    event.originalEvent.dataTransfer.setData("text", event.currentTarget.id);
  }

  function drop(event) {
    event.preventDefault();
    const task_id = event.originalEvent.dataTransfer.getData("text");
    const new_parent_id = event.currentTarget.id;

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
