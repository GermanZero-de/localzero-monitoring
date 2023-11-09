document.getElementById("nav-burger").addEventListener("click", toggleMobile);
document
  .getElementById("menu-item-toggleable")
  .addEventListener("click", toggleSubmenu);

function toggleMobile() {
  document.getElementById("site-menu").classList.toggle("shownow");
}

function toggleSubmenu(event) {
  var liElement = event.currentTarget;
  var ulElement = liElement.querySelector("ul"); // Find the first <ul> child element

  if (ulElement) {
    ulElement.classList.toggle("show-sub-menu"); // Toggle the class 'submenu-open' on the <ul> element
  }
}
