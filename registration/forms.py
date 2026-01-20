import django_filters
from django import forms
from item.models import Item
from inventory.models import Room
from .models import Record
from .choices import ConservationState
from core import widgets 
from django.contrib.auth import get_user_model

User = get_user_model()

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

    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        required=False,
        widget=widgets.Select(
            label="Sala",
            label_class="form-field-label",
            input_class="form-field-input",
        ),
    )

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

    def __init__(self, *args, institution=None, **kwargs):
        super().__init__(*args, **kwargs)

        if institution:
            self.fields["room"].queryset = Room.objects.filter(
                institution=institution
            )

class RecordFilter(django_filters.FilterSet):

    item__name = django_filters.CharFilter(
        lookup_expr = 'icontains',
        widget = widgets.InputField(label="Item", type="text", 
        label_class="label-text", input_class="filter-input two-thirds-input")
    )
    item__serial = django_filters.CharFilter(
        lookup_expr = 'icontains',
        widget=widgets.InputField(label="Serial", type="text", 
        label_class="label-text", input_class="filter-input three-line-input custom-arrow")
    )
    conservation_state = django_filters.ChoiceFilter(
        choices=ConservationState.choices,
        widget=widgets.Select(label="Estado de conservação", 
        label_class="label-text", input_class="filter-input two-line-input custom-arrow")
    )
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=widgets.Select(label="Criador", 
        label_class="label-text", input_class="filter-input two-line-input custom-arrow")
    )
    item__room = django_filters.ModelChoiceFilter(
        queryset=Room.objects.all(),
        widget=widgets.Select(label="Sala", 
        label_class="label-text", input_class="filter-input three-line-input custom-arrow")
    )
    item__created_at = django_filters.CharFilter(
        field_name="item__created_at",
        lookup_expr="gte",
        widget=widgets.InputField(label="Data de criação (item)", type="date",
        label_class="label-text", input_class="date-input filter-input three-line-input custom-date"),
    )
    recorded_at = django_filters.CharFilter(
        field_name="recorded_at",
        lookup_expr="gte",
        widget=widgets.InputField(label="Data de registro", type="date",
        label_class="label-text", input_class="date-input filter-input three-line-input custom-date"),
    )

    class Meta:
        model = Record
        fields = [
            "item__name",
            "item__serial",
            "conservation_state",
            "user",
            "item__room",
            "item__created_at",
            "recorded_at",
        ]