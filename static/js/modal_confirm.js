(() => {
  const openModalConfirmButtons = document.querySelectorAll(
    "[data-open-modal-confirm]",
  );

  for (const button of openModalConfirmButtons) {
    const id = button.dataset["openModalConfirm"];

    const modal = document.querySelector(`[data-confirm-modal='${id}']`);

    console.log(modal);

    modal.addEventListener("click", (e) => {
      if (e.target == modal) {
        modal.classList.remove("active");
      }
    });

    button.addEventListener("click", () => {
      modal.classList.add("active");
    });

    modal.querySelector("#removeModalCloseBtn").onclick = () => {
      modal.classList.remove("active");
    };

    modal.querySelector("#removeModalCancelBtn").onclick = () => {
      modal.classList.remove("active");
    };
  }
})();
