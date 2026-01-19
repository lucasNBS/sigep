document.addEventListener("DOMContentLoaded", () => {

  const inputs = document.querySelectorAll(".input-field-reset");
  const hiddenCode = document.getElementById("otp-code");
  const form = document.querySelector("form.login-form");

  if (!inputs.length || !hiddenCode || !form) return;

  function syncHiddenCode() {
    hiddenCode.value = Array.from(inputs)
      .map((i) => (i.value || "").replace(/\D/g, "").slice(0, 1))
      .join("");
  }

  inputs.forEach((input, index) => {
    input.addEventListener("input", (event) => {
      event.target.value = (event.target.value || "").replace(/\D/g, "").slice(0, 1);

      syncHiddenCode();

      if (event.target.value.length === 1) {
        if (index < inputs.length - 1) {
          inputs[index + 1].focus();
          inputs[index + 1].classList.add("input-field-reset-has-value");
        } else {
          const btn = document.querySelector(".login-button-link");
          if (btn) btn.focus();
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

    input.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && !input.value && index > 0) {
        inputs[index - 1].focus();
      }
    });

    input.addEventListener("paste", (e) => {
      const pasted = (e.clipboardData || window.clipboardData).getData("text");
      const digits = (pasted || "").replace(/\D/g, "").slice(0, inputs.length);
      if (!digits) return;

      e.preventDefault();
      digits.split("").forEach((d, i) => {
        inputs[i].value = d;
        inputs[i].classList.add("input-field-reset-has-value");
      });

      syncHiddenCode();

      const last = Math.min(digits.length, inputs.length) - 1;
      if (last >= 0) inputs[last].focus();
    });
  });

  form.addEventListener("submit", () => {
    syncHiddenCode();
  });
});
