$(document).ready(function () {
  $(".cap_board__task-item").on("dragstart", function (ev) {
    drag(ev);
  });

  $(".cap_board__task-area")
    .on("dragover", function (ev) {
      allowDrop(ev);
    })
    .on("drop", function (ev) {
      drop(ev, this);
    });

  function allowDrop(ev) {
    ev.preventDefault();
  }

  function drag(ev) {
    ev.originalEvent.dataTransfer.setData("text", ev.target.id);
  }

  function drop(ev) {
    ev.preventDefault();
    const task_id = ev.originalEvent.dataTransfer.getData("text");
    const column_id = ev.target.id;

    const task_pk = task_id.split("-")[1];
    const column_pk = column_id.split("-")[1];

    updateTask(task_pk, column_pk);
  }

  function updateTask(task_pk, column_pk) {
    const csrftoken = document.querySelector(
      "[name=csrfmiddlewaretoken]",
    ).value;

    $.ajax({
      url: "/admin/cap/task/update/" + task_pk + "/",
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      mode: "same-origin", // do not send the CSRF token to another domain
      data: { task_pk: task_pk, new_parent_pk: column_pk },
    }).done(function (data) {
      console.log(data);
    });
  }
});
