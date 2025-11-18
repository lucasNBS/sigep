function attachDropdown(buttonId, menuId) {
  const btn = document.getElementById(buttonId);
  const menu = document.getElementById(menuId);

  if (!btn || !menu) return;

  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const isOpen = menu.style.display === "block";
    menu.style.display = isOpen ? "none" : "block";
  });

  document.addEventListener("click", (e) => {
    if (!btn.contains(e.target) && !menu.contains(e.target)) {
      menu.style.display = "none";
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  attachDropdown("btn-user-menu", "dropdown-user");
  attachDropdown("btn-numbers", "dropdown-numbers");
  attachDropdown("btn-scan", "dropdown-scan");
});
