from django import forms
from . import models
from institution import models as institution_models

class InventoryForm(forms.ModelForm):
    class Meta:
        model = models.Inventory
        fields = ["title", "leader_consultor", "consultors", "rooms"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-field-input",
                "placeholder": "Inventário Anual 2025",
            }),
            "leader_consultor": forms.Select(attrs={
                "class": "form-field-input",
            }),
            "consultors": forms.SelectMultiple(attrs={
                "class": "form-field-input",
            }),
            "rooms": forms.SelectMultiple(attrs={
                "class": "form-field-input",
            }),
        }

            