from django import forms
from .models import Institution

class InstitutionForm(forms.ModelForm):
  class Meta:
        model = Institution
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
    