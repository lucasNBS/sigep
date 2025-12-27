from django import forms
from . import models
from institution import models as institution_models
from django.contrib.auth import get_user_model

User = get_user_model()

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



class InventoryFilterForm(forms.Form):
    title = forms.CharField(
        required=False,
        label="Título",
        widget=forms.TextInput(attrs={
            "class": "filter-input two-thirds-input",
            "placeholder": "Título do inventário"
        })
    )
    responsible = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Aberto por",
        widget=forms.Select(attrs={
            "class": "filter-input three-line-input custom-arrow"
        })
    )
    leader_consultor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Consultor líder",
        widget=forms.Select(attrs={
            "class": "filter-input two-line-input custom-arrow"
        })
    )
    consultor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Consultor",
        widget=forms.Select(attrs={
            "class": "filter-input two-line-input custom-arrow"
        })
    )
    status = forms.ChoiceField(
        choices=[("", "---------")] + list(models.Inventory._meta.get_field("status").choices),
        required=False,
        widget=forms.Select(attrs={
            "class": "filter-input three-line-input custom-arrow"
        })
    )
    date_start = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "date-input filter-input three-line-input custom-date"
        })
    )
    date_end = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "date-input filter-input three-line-input custom-date"
        })
    )

            