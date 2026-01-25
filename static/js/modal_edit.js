(() => {
  const openInstitutionEditButtons = document.querySelectorAll(
    "[data-open-institution-edit-modal]",
  );

  for (const button of openInstitutionEditButtons) {
    const id = button.dataset["openInstitutionEditModal"];

    const modal = document.querySelector(`[data-edit-modal='${id}']`);

    const nome = modal.querySelector("#edit-nome");
    const file = modal.querySelector("#logo-input");
    const fileName = modal.querySelector("#logo-filename");

    function open(instId, instNome = "") {
      if (nome) nome.value = instNome || "";
      if (file) file.value = "";
      if (fileName) fileName.textContent = "Selecione uma imagem…";
      modal.classList.add("active");
    }

    function close() {
      modal.classList.remove("active");
    }

    modal.querySelector("#editModalCloseBtn")?.addEventListener("click", close);
    modal
      .querySelector("#editModalCancelBtn")
      ?.addEventListener("click", close);

    modal.addEventListener("mousedown", (e) => {
      if (e.target === modal) close();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal.classList.contains("active")) close();
    });

    file?.addEventListener("change", () => {
      fileName.textContent = file.files?.[0]?.name || "Selecione uma imagem…";
    });

    button.addEventListener("click", () => {
      open();
    });
  }
})();
