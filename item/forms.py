import django_filters
from django import forms
from django.core.exceptions import ValidationError

from core import widgets, utils
from institution.models import Category, Institution
from inventory.models import Room
from registration.choices import ConservationState

from . import models, choices

class ItemForm(forms.ModelForm):
  name = forms.CharField(
    label="Nome",
    widget=widgets.InputField(label="Nome", type="text", 
    label_class="form-field-label", input_class="form-field-input")
  )
  description = forms.CharField(
    label="Descrição",
    required=False,
    widget=widgets.Textarea(
      label="Descrição", placeholder="Características principais",
      label_class="form-field-label", input_class="form-field-input"
    )
  )
  serial = forms.CharField(
    label="Serial",
    widget=widgets.InputField(label="Serial", type="text",
    label_class="form-field-label", input_class="form-field-input")
  )
  invoice_key = forms.CharField(
    label="Nota Fiscal",
    widget=widgets.InputField(
      label="Nota Fiscal",
      type="text",
      label_class="form-field-label", input_class="form-field-input"
    )
  )
  notes = forms.CharField(
    label="Observações",
    required=False,
    widget=widgets.Textarea(label="Observações", placeholder="Informações adicionais",
    label_class="form-field-label", input_class="form-field-input")
  )
  category_name = forms.CharField(label="Categoria", widget=forms.HiddenInput())
  room_name = forms.CharField(label="Sala", widget=forms.HiddenInput())

  class Meta:
    model = models.Item
    fields = ["name", "description", "serial", "invoice_key", "notes", "category", "room"]
    widgets = {
      "category": widgets.Autocomplete(label="Categoria", autocomplete="categorias", editable=True,
                                    label_class="form-field-label", input_class="form-field-input"),
      "room": widgets.Autocomplete(label="Sala", autocomplete="salas", editable=True,
                                    label_class="form-field-label", input_class="form-field-input")
    }

  def clean(self):
    clean_data = super().clean()

    room = utils.handle_selected_element(
      Room, self.data.get("room"), self.data.get("room_name")
    )
    clean_data["room"] = room

    category = utils.handle_selected_element(
      Category, self.data.get("category"), self.data.get("category_name")
    )
    clean_data["category"] = category

    return clean_data

  def _handle_category_and_room_left(self, instance, old_instance):
    is_there_old_category_to_delete = False
    if instance.category.id != old_instance.category.id:
      if models.Item.objects.filter(category=old_instance.category).count() == 1:
        is_there_old_category_to_delete = True

    is_there_old_room_to_delete = False
    if instance.room.id != old_instance.room.id:
      if models.Item.objects.filter(room=old_instance.room).count() == 1:
        is_there_old_room_to_delete = True

    instance.save()

    if is_there_old_category_to_delete:
      old_instance.category.delete()
    if is_there_old_room_to_delete:
      old_instance.room.delete()

  def save(self):
    instance = super().save(commit=False)

    old_instance = None
    if instance.id:
      old_instance = models.Item.objects.filter(id=instance.id).first()

    self.instance.institution = Institution.objects.get(id=1)

    if old_instance:
      self._handle_category_and_room_left(instance, old_instance)
    else:
      instance.save()

    return instance


class ItemFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(
    lookup_expr="icontains",
    widget=widgets.InputField(label="Nome", type="text",
    label_class="label-text", input_class=""),
  )
  serial = django_filters.CharFilter(
    lookup_expr="exact",
    widget=widgets.InputField(label="Serial", type="text",
    label_class="label-text", input_class="form-field-input"),
  )
  category = django_filters.ModelChoiceFilter(
    queryset=Category.objects.all(),
    widget=widgets.Autocomplete(label="Categoria", autocomplete="categorias",
    label_class="label-text", input_class="form-field-input"),
  )
  room = django_filters.ModelChoiceFilter(
    queryset=Room.objects.all(),
    widget=widgets.Autocomplete(label="Sala", autocomplete="salas",
    label_class="label-text", input_class="form-field-input"),
  )
  date_start = django_filters.CharFilter(
    field_name="created_at",
    lookup_expr="gte",
    widget=widgets.InputField(label="Data de Cadastro (Início)", type="date",
    label_class="label-text", input_class="form-field-input"),
  )
  date_end = django_filters.CharFilter(
    field_name="created_at",
    lookup_expr="lte",
    widget=widgets.InputField(label="Data de Cadastro (Fim)", type="date",
    label_class="label-text", input_class="form-field-input"),
  )
  status = django_filters.ChoiceFilter(
    choices=choices.Status,
    widget=widgets.Select(label="Status",
    label_class="label-text", input_class="form-field-input"),
  )
  conservation_state = django_filters.ChoiceFilter(
    choices=ConservationState,
    widget=widgets.Select(label="Estado de Conservação",
    label_class="label-text", input_class="form-field-input"),
  )
  is_deleted = django_filters.BooleanFilter(
    widget=widgets.Select(label="Estado de Ativação", choices=choices.ACTIVE_STATUS,
    label_class="label-text", input_class="form-field-input"),
  )

  class Meta:
    model = models.Item
    fields = [
      "name",
      "serial",
      "category",
      "room",
      "date_start",
      "date_end",
      "status",
      "conservation_state",
      "is_deleted",
    ]

class ItemImport(forms.Form):
  spreadsheet = forms.FileField(label="Arquivo")
  ALLOWED_EXTENSIONS = ["xls", "xlsx", "csv", "ods"]

  def clean_spreadsheet(self):
    spreadsheet = self.cleaned_data["spreadsheet"]
    if spreadsheet.name.split('.')[-1] not in self.ALLOWED_EXTENSIONS:
      raise ValidationError("Tipo de arquivo inválido")
    return spreadsheet

