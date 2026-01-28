{
  const convert_type = {
    categoria: "category",
    sala: "room",
  };

  function createDropdownElement(option) {
    const dropdownElement = document.createElement("div");

    dropdownElement.classList.add("autocomplete-option");
    dropdownElement.dataset.value = option.id;
    dropdownElement.innerText = option.name;

    return dropdownElement;
  }

  function createCheckbox(optionId, type) {
    const checkbox = document.createElement("input");

    checkbox.setAttribute("type", "checkbox");
    checkbox.setAttribute("name", convert_type[type]);
    checkbox.setAttribute("id", `id_${convert_type[type]}`);
    checkbox.setAttribute("value", optionId);

    return checkbox;
  }

  class Autocomplete {
    constructor(element, editable) {
      this.element = element;
      this.url = element.dataset.autocomplete;
      this.id = element.dataset.institutionId;
      this.input = element.querySelector("[data-autocomplete-input]");
      this.suggestionsContainer = element.querySelector(
        "[data-autocomplete-suggestions]",
      );
      this.unselect = element.querySelector("[data-autocomplete-unselect]");
      this.nameInput = element.parentNode.querySelector("[type='hidden']");
      this.editable = editable;
      this.init();
    }

    init() {
      let timeout;
      this.input.addEventListener("keyup", () => {
        if (this.editable) {
          this.nameInput.value = this.input.value;
        }

        if (this.unselect) {
          return;
        }

        clearTimeout(timeout);
        this.suggestionsContainer.innerHTML = "";

        timeout = setTimeout(async () => await this.search(this.input), 600);
      });

      if (this.unselect) {
        this.unselect.addEventListener("click", () => {
          this.unselectOption(this.unselect);
        });

        this.checkbox = this.selectOption({
          name: this.unselect.dataset.label,
          id: this.unselect.dataset.value,
        });
      }

      document.addEventListener("click", (event) => {
        const clickedElement = event.target;
        if (
          !(
            clickedElement.dataset.autocompleteInput ||
            clickedElement.dataset.autocompleteSugestions
          )
        ) {
          this.suggestionsContainer.innerHTML = "";
        }
      });
    }

    async search(input) {
      if (input.value.length === 0) {
        return;
      }

      const results = await fetch(
        `https://sigep.todpig.com.br/instituicao/${this.id}/${this.url}/autocomplete/?search=${input.value}`,
      ).then((res) => res.json());

      results.forEach((option) => {
        const dropdownElement = createDropdownElement(option);
        this.suggestionsContainer.append(dropdownElement);

        dropdownElement.addEventListener("click", () => {
          this.selectOption(option, true);
        });
      });
    }

    selectOption(option, shouldCreateNewUnselectOptionButton = false) {
      this.input.value = option.name;
      if (this.editable) {
        this.nameInput.value = option.name;
      } else {
        this.input.setAttribute("disabled", "true");
      }
      const checkbox = createCheckbox(option.id, this.url);
      this.input.append(checkbox);
      checkbox.click();
      if (shouldCreateNewUnselectOptionButton) {
        this.createNewUnselectOptionButton();
      }
      this.suggestionsContainer.innerHTML = "";
      return checkbox;
    }

    createNewUnselectOptionButton() {
      const newUnselectOptionButton = document.createElement("span");
      newUnselectOptionButton.classList.add("autocomplete-unselect");
      this.unselect = newUnselectOptionButton;

      newUnselectOptionButton.addEventListener("click", () => {
        this.unselectOption();
      });
      newUnselectOptionButton.innerHTML = "&times;";

      this.element.append(newUnselectOptionButton);
    }

    unselectOption() {
      this.unselect.remove();
      this.unselect = null;
      this.input.value = "";
      if (this.editable) {
        this.nameInput.value = "";
      } else {
        this.input.removeAttribute("disabled");
      }
      this.checkbox.click();
    }
  }

  const autocompletes = document.querySelectorAll("[data-autocomplete]");

  autocompletes.forEach((autocomplete) => {
    new Autocomplete(
      autocomplete,
      autocomplete.dataset["autocompleteEditable"],
    );
  });
}
