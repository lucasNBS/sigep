const inputs = document.querySelectorAll(".input-field-reset");

inputs.forEach((input, index) => {
  input.addEventListener("input", (event) => {
    if (!/^[0-9]$/.test(event.target.value) && event.target.value !== "") {
      event.target.value = "";
      return;
    }

    if (event.target.value <= 0) {
      inputs[index - 1].focus();
      inputs[index - 1].classList.remove("input-field-reset-has-value");
    }

    if (event.target.value.length === 1) {
      if (index < inputs.length - 1) {
        inputs[index + 1].focus();
        inputs[index + 1].classList.add("input-field-reset-has-value");
      } else {
        // último input: direcionar foco para o link de login
        const loginLink = document.querySelector(".login-button-link");
        if (loginLink) {
          loginLink.focus();
        }
      }
    } else if (event.target.value.length === 0 && index > 0) {
      inputs[index - 1].focus();
      inputs[index - 1].classList.remove("input-field-reset-has-value");
    }

    if (event.target.value.length > 0) {
      input.classList.add("input-field-reset-has-value");
    } else {
      input.classList.remove("input-field-reset-has-value");
    }
  });
});
