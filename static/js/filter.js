{
  function openFilter() {
    document.getElementById("filterModal").classList.add("active");
  }

  function closeFilter() {
    document.getElementById("filterModal").classList.remove("active");
  }

  const openFilterModalButton = document.querySelector(
    "[data-open-modal-filter]"
  );

  openFilterModalButton.addEventListener("click", openFilter);

  const closeFilterModalButtons = document.querySelectorAll(
    "[data-close-filter-modal]"
  );

  for (const button of closeFilterModalButtons) {
    button.addEventListener("click", (e) => {
      if (e.target.dataset["closeFilterModal"] != undefined) {
        closeFilter();
      }
    });
  }
}
