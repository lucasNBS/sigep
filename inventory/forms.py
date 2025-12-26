from django import forms
from . import models
from institution import models as institution_models

class InventoryForm(forms.ModelForm):
    class Meta:
        model = models.Inventory
        fields = ["title","institution", "leader_consultor", "consultors", "rooms"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-field-input",
                "placeholder": "Inventário Anual 2025",
            }),
            "institution": forms.Select(attrs={
                "class": "form-field-input",
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["institution"].queryset = institution_models.Institution.objects.filter(permissions__user=user)
            