from django import forms
from . import models

class InstitutionForm(forms.ModelForm):
  class Meta:
        model = models.Institution
        fields = ["name", "logo_url"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Nome",
            }),
            "logo_url": forms.FileInput(attrs={
                "class": "logo-filename",
            }),
        }
    