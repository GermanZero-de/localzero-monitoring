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
    ev.originalEvent.dataTransfer.setData(
      "form",
      ev.target.getElementsByTagName("form"),
    );
  }

  function drop(ev) {
    ev.preventDefault();
    const task_id = ev.originalEvent.dataTransfer.getData("text");
    const column_id = ev.target.id;

    console.log(task_id + " " + column_id);

    const task_pk = task_id.split("-")[1];
    updateTask(task_pk);
  }

  function updateTask(pk) {
    const form_data = $("#task-" + pk).serialize();

    $.ajax({
      url: "/admin/cap/task/update/" + pk + "/",
      method: "POST",
      data: { path: "00060002", depth: 2 }, // TODO
    }).done(function (data) {
      console.log(data);
    });
  }
});
