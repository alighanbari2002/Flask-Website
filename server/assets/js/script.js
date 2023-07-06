let targets = document.querySelectorAll("li");
let main, sub;
targets.forEach(function(target) {
  if (target.parentElement.parentElement.tagName == "DIV") { // for mains
    target.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
      let subMenu = target.querySelector("ul");
      toggleClass(subMenu);
      if (main && main != subMenu) {
        main.classList.remove("show")
      }
      main = subMenu;
    });
  } else if (target.parentElement.parentElement.parentElement.parentElement.tagName == "DIV") {
    target.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
      let subMenu = target.querySelector("ul");
      toggleClass(subMenu);
      if (sub && sub != subMenu) {
        sub.classList.remove("show")
      }
      sub = subMenu;
    });
  } else {
    target.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
    });
  }
});

function toggleClass(subMenu) {
  if (subMenu.className.includes('show')) {
    subMenu.classList.remove("show")
  } else {
    subMenu.classList.add("show");
  }
}