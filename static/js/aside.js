{
  const aside = document.querySelector(".aside");
  const asideBackground = document.querySelector(".aside-background");
  const asideButton = document.querySelector(".menu-image");

  document.body.addEventListener("click", (e) => {
    if (e.target.closest(".aside.open") == null && e.target != asideButton) {
      aside.classList.remove("open");
      asideBackground.classList.remove("open");
    }
  });

  asideButton.addEventListener("click", () => {
    aside.classList.toggle("open");
    asideBackground.classList.toggle("open");
  });
}
