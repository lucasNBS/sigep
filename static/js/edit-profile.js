function openModal() {
  document.getElementById("editProfileModal").classList.add("active");
}

function closeModal() {
  document.getElementById("editProfileModal").classList.remove("active");
}

const openProfileEditButtons = document.querySelectorAll(
  "[data-open-profile-modal]",
);
for (const button of openProfileEditButtons) {
  button.addEventListener("click", openModal);
}

const closeProfileEditButtons = document.querySelectorAll(
  "[data-close-profile-modal]",
);
for (const button of closeProfileEditButtons) {
  button.addEventListener("click", (e) => {
    if (e.target.closest("[data-close-profile-modal]") != undefined) {
      closeModal();
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const dropzone = document.getElementById("photo-dropzone");
  const fileInput = document.getElementById("id_photo_url");
  const filenameEl = document.getElementById("logo-filename");

  if (!dropzone || !fileInput) return;

  const openPicker = () => fileInput.click();

  dropzone.addEventListener("click", openPicker);

  dropzone.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      openPicker();
    }
  });

  fileInput.addEventListener("change", () => {
    const f = fileInput.files && fileInput.files[0];
    if (filenameEl)
      filenameEl.textContent = f ? f.name : "Selecione uma imagem…";
  });
});
