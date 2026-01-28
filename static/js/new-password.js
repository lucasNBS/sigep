function togglePassword1Visibility() {
  const passwordInput1 = document.getElementById("new_password1");

  const toggleButton1 = document.querySelector(
    ".toggle-password-visibility-1 img",
  );

  if (passwordInput1.type === "password") {
    passwordInput1.type = "text";
    toggleButton1.src = "/static/icons/Eye.svg";
  } else {
    passwordInput1.type = "password";
    toggleButton1.src = "/static/icons/CrossedEye.svg";
  }
}

function togglePassword2Visibility() {
  const passwordInput2 = document.getElementById("new_password2");

  const toggleButton2 = document.querySelector(
    ".toggle-password-visibility-2 img",
  );

  if (passwordInput2.type === "password") {
    passwordInput2.type = "text";
    toggleButton2.src = "/static/icons/Eye.svg";
  } else {
    passwordInput2.type = "password";
    toggleButton2.src = "/static/icons/CrossedEye.svg";
  }
}

document
  .querySelector(".toggle-password-visibility-1")
  .addEventListener("click", togglePassword1Visibility);

document
  .querySelector(".toggle-password-visibility-2")
  .addEventListener("click", togglePassword2Visibility);
