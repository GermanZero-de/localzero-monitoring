const progressbars = document.querySelectorAll("div.progress-bar");

progressbars.forEach(pb => {
  pb.style.width = pb.dataset.value + "%";
});
