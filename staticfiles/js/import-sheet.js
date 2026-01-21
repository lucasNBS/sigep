function openModal() {
  document.getElementById("invitationModal").classList.add("active");
}

function closeModal() {
  document.getElementById("invitationModal").classList.remove("active");
}

const openImportModalButton = document.querySelector(
  "[data-open-modal-import]"
);

openImportModalButton.addEventListener("click", openModal);

const closeImportModalButtons = document.querySelectorAll(
  "[data-close-import-modal]"
);

for (const button of closeImportModalButtons) {
  button.addEventListener("click", (e) => {
    if (e.target.dataset["closeImportModal"] != undefined) {
      closeModal();
    }
  });
}
