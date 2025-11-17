(() => {
  const modal = document.getElementById("registerItemModal");
  const form = document.getElementById("form-register-item");

  function open(serial = "") {
    modal.classList.add("active");
  }

  function close() {
    modal.classList.remove("active");
  }

  window.openRegisterItemModal = open;

  document
    .getElementById("registerItemModalCloseBtn")
    ?.addEventListener("click", close);

  document
    .getElementById("registerItemModalCancelBtn")
    ?.addEventListener("click", close);

<<<<<<< Updated upstream
  modal.addEventListener('mousedown', (e) => {
=======
  // Close modal when clicking outside of it
  modal.addEventListener("mousedown", (e) => {
>>>>>>> Stashed changes
    if (e.target === modal) close();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("active")) {
      close();
    }
  });

  const openRegisterItemButtons = document.querySelectorAll(
    "[data-open-register-item-modal]"
  );

  for (const button of openRegisterItemButtons) {
    button.addEventListener("click", open);
  }
})();
