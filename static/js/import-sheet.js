function openModal() {
  document.getElementById("invitationModal").classList.add("active");
}

function closeModal() {
  document.getElementById("invitationModal").classList.remove("active");
}

const openImportModalButton = document.querySelector(
  "[data-open-modal-import]",
);

openImportModalButton.addEventListener("click", openModal);

const closeImportModalButtons = document.querySelectorAll(
  "[data-close-import-modal]",
);

for (const button of closeImportModalButtons) {
  button.addEventListener("click", (e) => {
    if (e.target.dataset["closeImportModal"] != undefined) {
      closeModal();
    }
  });
}

const fileInput = document.querySelector("#logo-input");
const fileIndicator = document.querySelector("#logo-filename");

fileInput.addEventListener("change", (e) => {
  if (e.target.value) {
    fileIndicator.innerHTML =
      e.target.value.split("\\")[e.target.value.split("\\").length - 1];
  } else {
    fileIndicator.innerHTML = "Escolher Arquivo";
  }
});
