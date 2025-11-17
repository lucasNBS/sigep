(() => {
  const modal = document.getElementById("removeModal");
  const form = document.getElementById("form-remove");

  function open(instId, instNome = "") {
    modal.classList.add("active");
  }

  function close() {
    modal.classList.remove("active");
  }

  window.openRemoveModal = open;

  // close for buttons and outside click
  document
    .getElementById("removeModalCloseBtn")
    ?.addEventListener("click", close);
  document
    .getElementById("removeModalCancelBtn")
    ?.addEventListener("click", close);
  modal.addEventListener("mousedown", (e) => {
    if (e.target === modal) close();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("active")) close();
  });

  const openInstitutionRemoverButtons = document.querySelectorAll(
    "[data-open-institution-remove-modal]"
  );

  for (const button of openInstitutionRemoverButtons) {
    button.addEventListener("click", open);
  }
})();
