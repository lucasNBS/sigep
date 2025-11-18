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

  modal.addEventListener("mousedown", (e) => {
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
