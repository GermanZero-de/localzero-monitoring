const progressbars = document.querySelectorAll("div.progress-bar");

progressbars.forEach((pb) => {
  pb.style.width = pb.dataset.value + "%";
});

$('[data-bs-toggle="tooltip"]').click(function (e) {
  e.preventDefault();
});
