from django import forms
from item.models import Item
from .models import Record
from .choices import ConservationState
from core import widgets 

class RegisterSerialForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["serial"]
        widgets = {
            "serial": forms.TextInput(attrs={
                "class": "input",
            }),
        }

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["notes","conservation_state"]
        widgets = {
            "notes": widgets.Textarea(
                label_class = "form-field-label",
                input_class = "form-field-textarea",
                placeholder = "Informe as características princípais do equipamento",
                label = "Descrição",
            ),
            "conservation_state": widgets.Select(
                label_class = "form-field-label",
                input_class = "form-field-input",
                label = "Estado de conservação",
            ),
        }
