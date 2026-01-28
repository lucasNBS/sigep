import django_filters
from core import widgets
from django import forms
from .models import Inventory, Room  
from .choices import Status
from institution import models as institution_models
from django.contrib.auth import get_user_model

User = get_user_model()

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
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

    def __init__(self, *args, **kwargs):
        self.institution_id = kwargs.pop('institution_id')
        self.user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)
        self.fields["rooms"].queryset = Room.objects.filter(institution__id=self.institution_id)
        self.fields["leader_consultor"].queryset = User.objects.filter(
            permissions__institution__id=self.institution_id
        ).distinct()
        self.fields["consultors"].queryset = User.objects.filter(
            permissions__institution__id=self.institution_id
        ).distinct()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.institution = institution_models.Institution.objects.get(id=self.institution_id)
        instance.responsible = User.objects.get(id=self.user_id)
        instance.save()
        self.save_m2m()
        return instance


            
class InventoryFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        lookup_expr = 'icontains',
        widget = widgets.InputField(label="Título", type="text", 
        label_class="label-text", input_class="filter-input two-thirds-input")
    )
    responsible = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=widgets.Select(label="Criado por", 
        label_class="label-text", input_class="filter-input three-line-input custom-arrow")
    )
    leader_consultor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=widgets.Select(label="Consultor líder", 
        label_class="label-text", input_class="filter-input two-line-input custom-arrow")
    )
    consultors = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=widgets.Select(label="Consultor", 
        label_class="label-text", input_class="filter-input two-line-input custom-arrow")
    )
    status = django_filters.ChoiceFilter(
        choices=Status.choices,
        widget=widgets.Select(label="Status", label_class="label-text", input_class="filter-input three-line-input custom-arrow")
    )
    date_start = django_filters.CharFilter(
        field_name="created_at",
        lookup_expr="gte",
        widget=widgets.InputField(label="Data de Cadastro (Início)", type="date",
        label_class="label-text", input_class="date-input filter-input three-line-input custom-date"),
    )
    date_end = django_filters.CharFilter(
        field_name="created_at",
        lookup_expr="lte",
        widget=widgets.InputField(label="Data de Cadastro (Fim)", type="date",
        label_class="label-text", input_class="date-input filter-input three-line-input custom-date"),
    )

    class Meta:
        model = Inventory
        fields = [
            "title",
            "responsible",
            "leader_consultor",
            "consultors",
            "date_start",
            "date_end",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        self.institution_id = kwargs.pop('institution_id')
        super().__init__(*args, **kwargs)
        self.filters["leader_consultor"].queryset = User.objects.filter(
            permissions__institution__id=self.institution_id
        ).distinct()
        self.filters["consultors"].queryset = User.objects.filter(
            permissions__institution__id=self.institution_id
        ).distinct()
        self.filters["responsible"].queryset = User.objects.filter(
            permissions__institution__id=self.institution_id
        ).distinct()
