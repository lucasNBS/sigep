function togglePasswordVisibility() {
  const passwordInput = document.getElementById("password");
  const toggleButton = document.querySelector(
    ".toggle-password-visibility img"
  );

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    toggleButton.src = "/static/icons/Eye.svg";
  } else {
    passwordInput.type = "password";
    toggleButton.src = "/static/icons/CrossedEye.svg";
  }
}

document
  .querySelector(".toggle-password-visibility")
  .addEventListener("click", togglePasswordVisibility);
