import django_filters
from django import forms

from core import widgets
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
      "category": widgets.Autocomplete(
        label="Categoria",
        autocomplete="categoria",
        editable=True,
        label_class="form-field-label",
        input_class="form-field-input"
      ),
      "room": widgets.Autocomplete(
        label="Sala",
        autocomplete="sala",
        editable=True,
        label_class="form-field-label",
        input_class="form-field-input"
      )
    }

  def __init__(self, *args, **kwargs):
    self.institution_id = kwargs.pop('institution_id')
    super().__init__(*args, **kwargs)

  def clean(self):
    clean_data = super().clean()

    room = self._handle_selected_element(
      Room, self.data.get("room"), self.data.get("room_name")
    )
    clean_data["room"] = room

    category = self._handle_selected_element(
      Category, self.data.get("category"), self.data.get("category_name")
    )
    clean_data["category"] = category

    return clean_data

  def _handle_selected_element(self, model, element_id, element_name):
    if (element_id):
      element = model.objects.get(id=element_id)
      element.name = element_name
      element.save(update_fields=["name"])
      element.refresh_from_db()
    else:
      element = model(
        name=element_name, institution=Institution.objects.get(id=self.institution_id)
      )
      element.full_clean()
      element.save()
    return element

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

    self.instance.institution = Institution.objects.get(id=self.institution_id)

    if old_instance:
      self._handle_category_and_room_left(instance, old_instance)
    else:
      instance.save()

    return instance


class ItemFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(
    lookup_expr="icontains",
    widget=widgets.InputField(label="Nome", type="text",
    label_class="label-text", input_class="filter-input"),
  )
  serial = django_filters.CharFilter(
    lookup_expr="exact",
    widget=widgets.InputField(label="Serial", type="text",
    label_class="label-text", input_class="filter-input"),
  )
  category = django_filters.ModelChoiceFilter(
    queryset=Category.objects.all(),
    widget=widgets.Autocomplete(label="Categoria", autocomplete="categoria",
    label_class="label-text", input_class="filter-input"),
  )
  room = django_filters.ModelChoiceFilter(
    queryset=Room.objects.all(),
    widget=widgets.Autocomplete(label="Sala", autocomplete="sala",
    label_class="label-text", input_class="filter-input"),
  )
  date_start = django_filters.CharFilter(
    field_name="created_at",
    lookup_expr="gte",
    widget=widgets.InputField(label="Data de Cadastro (Início)", type="date",
    label_class="label-text", input_class="filter-input"),
  )
  date_end = django_filters.CharFilter(
    field_name="created_at",
    lookup_expr="lte",
    widget=widgets.InputField(label="Data de Cadastro (Fim)", type="date",
    label_class="label-text", input_class="filter-input"),
  )
  status = django_filters.ChoiceFilter(
    choices=choices.Status,
    widget=widgets.Select(label="Status",
    label_class="label-text", input_class="filter-input"),
  )
  conservation_state = django_filters.ChoiceFilter(
    choices=ConservationState,
    widget=widgets.Select(label="Estado de Conservação",
    label_class="label-text", input_class="filter-input"),
  )
  is_deleted = django_filters.BooleanFilter(
    widget=widgets.Select(label="Estado de Ativação", choices=choices.ACTIVE_STATUS,
    label_class="label-text", input_class="filter-input"),
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
