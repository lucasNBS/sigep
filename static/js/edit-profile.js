function openModal() {
  document.getElementById("editProfileModal").classList.add("active");
}

function closeModal() {
  document.getElementById("editProfileModal").classList.remove("active");
}

const openProfileEditButtons = document.querySelectorAll(
  "[data-open-profile-modal]"
);

for (const button of openProfileEditButtons) {
  button.addEventListener("click", openModal);
}

const closeProfileEditButtons = document.querySelectorAll(
  "[data-close-profile-modal]"
);

for (const button of closeProfileEditButtons) {
  button.addEventListener("click", (e) => {
    if (e.target.dataset["closeProfileModal"] != undefined) {
      closeModal();
    }
  });
}
