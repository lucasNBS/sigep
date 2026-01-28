(function () {
  const modal = document.getElementById("editUserRoleModal");
  if (!modal) return;

  const openButtons = document.querySelectorAll("[data-open-user-role-modal]");
  const closeBtn = document.getElementById("editUserRoleModalCloseBtn");
  const cancelBtn = document.getElementById("editUserRoleModalCancelBtn");

  const openModal = () => modal.classList.add("active");
  const closeModal = () => modal.classList.remove("active");

  openButtons.forEach((btn) => {
    btn.addEventListener("click", openModal);
  });

  if (closeBtn) closeBtn.addEventListener("click", closeModal);
  if (cancelBtn) cancelBtn.addEventListener("click", closeModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });
})();
