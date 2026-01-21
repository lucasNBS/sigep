import pandas as pd

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, View
from django.views.generic.edit import FormMixin

from core.settings import MAX_ERRORS
from core.utils import handle_selected_element, validate_dataframe_column
from core.views import BaseContextView, AccessMixin
from institution.models import Institution, Category
from inventory.models import Room
from registration.forms import RecordFilter

from .models import Item
from .forms import ItemForm, ItemFilter, ItemImport

class ListItemView(AccessMixin, BaseContextView, FormMixin, ListView):
  model = Item
  queryset = Item.all_objects
  template_name = "item/patrimony.html"
  form_class = ItemImport
  success_url = reverse_lazy("dashboard")

  def post(self, request, *args, **kwargs):
    self.object_list = self.get_queryset()
    form = self.get_form()

    if form.is_valid():
      return self.form_valid(form)

    return self.form_invalid(form)

  def form_valid(self, form):
    file = form.cleaned_data["spreadsheet"]

    try:
      df = pd.read_excel(file)
      errors = self.validate_dataframe(df)

      if len(errors) > 0:
        for error in errors[:MAX_ERRORS]:
          form.add_error(None, error)
        return self.form_invalid(form)

      self.save_itens(df)
    except Exception as e:
      form.add_error(None, str(e))
      return self.form_invalid(form)

    return super().form_valid(form)

  def validate_dataframe(self, df):
    errors = []

    columns = {
      "Nome", "Serial", "Nota Fiscal", "Categoria", "Sala", "Descrição", "Observações"
    }

    if not columns.issubset(df.columns):
      errors.append("Colunas inválidas")
      return errors

    errors.extend(validate_dataframe_column(df, "Nome"))
    errors.extend(validate_dataframe_column(df, "Serial"))
    errors.extend(validate_dataframe_column(df, "Nota Fiscal"))
    errors.extend(validate_dataframe_column(df, "Categoria"))
    errors.extend(validate_dataframe_column(df, "Sala"))

    df["Descrição"] = df["Descrição"].fillna("")
    df["Observações"] = df["Observações"].fillna("")

    return errors

  def save_itens(self, df):
    itens = []

    with transaction.atomic():
      for _, row in df.iterrows():
        institution = Institution.objects.get(id=1)

        category = Category.objects.filter(name=row["Categoria"], institution=institution).first()
        room = Room.objects.filter(name=row["Sala"], institution=institution).first()

        category = handle_selected_element(
          Category, category.id if category else None, row["Categoria"]
        )
        room = handle_selected_element(Room, room.id if room else None, row["Sala"])

        itens.append(
          Item(
            institution=institution,
            name=row["Nome"],
            serial=row["Serial"],
            invoice_key=row["Nota Fiscal"],
            category=category,
            room=room,
            description=row["Descrição"],
            notes=row["Observações"],
          )
        )

      Item.objects.bulk_create(itens)

  def dispatch(self, request, *args, **kwargs):
    self.check_has_manager_access()
    return super().dispatch(request, *args, **kwargs)

  def get_paginate_by(self, queryset):
    page_size = self.request.GET.get("size")
    if page_size:
      return page_size
    return 10

  def get_queryset(self):
    queryset = super().get_queryset()
    self.filterset = ItemFilter(self.request.GET, queryset=queryset)
    return self.filterset.qs.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10
    context["filter"] = self.filterset
    context["import_form"] = ItemImport()
    return context

class CreateItemView(AccessMixin, BaseContextView, CreateView):
  model = Item
  template_name = "item/patrimony-form.html"
  form_class = ItemForm
  title = "Cadastrar Item"
  button = "Cadastrar"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_manager_access()
    return super().dispatch(request, *args, **kwargs)

  def get_success_url(self):
    return reverse("item-list", kwargs={"institution_id": self.kwargs.get('institution_id')})

  def get_form_kwargs(self):
    form_kwargs = super().get_form_kwargs()
    form_kwargs["institution_id"] = self.kwargs.get('institution_id')
    return form_kwargs
  
class UpdateItemView(AccessMixin, BaseContextView, UpdateView):
  model = Item
  pk_url_kwarg = "item_id"
  queryset = Item.all_objects
  template_name = "item/patrimony-form.html"
  form_class = ItemForm
  title = "Editar Item"
  button = "Editar"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_manager_access()
    return super().dispatch(request, *args, **kwargs)

  def get_success_url(self):
    return reverse("item-list", kwargs={"institution_id": self.kwargs.get('institution_id')})

  def get_form_kwargs(self):
    form_kwargs = super().get_form_kwargs()
    form_kwargs["institution_id"] = self.kwargs.get('institution_id')
    return form_kwargs

class DetailItemView(AccessMixin, BaseContextView, DetailView):
  model = Item
  pk_url_kwarg = "item_id"
  queryset = Item.all_objects
  template_name = "item/patrimony-detail.html"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_manager_access()
    return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10

    filterset = RecordFilter(self.request.GET, queryset=self.object.records.all())
    paginator = Paginator(filterset.qs, context["size"])
    page_number = self.request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context["page_obj"] = page_obj
    context["records"] = page_obj.object_list
    context["filter"] = filterset
    context["specific_item"] = True

    return context

class DeleteItemView(AccessMixin, DeleteView):
  model = Item
  pk_url_kwarg = "item_id"
  template_name = "item/confirm-delete.html"
  success_url = reverse_lazy("dashboard")

  def dispatch(self, request, *args, **kwargs):
    self.check_has_manager_access()
    return super().dispatch(request, *args, **kwargs)

class DownloadItemSpreadSheetView(View):
  filepath = "static/media/PlanilhaItem.ods"
  filename = "PlanilhaItem.ods"

  def get(self, request, *args, **kwargs):
    with open(self.filepath, "rb") as f:
      file = f.read()

    response = HttpResponse(file, content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = f"attachment; filename={self.filename}"

    return response

class RestoreItemView(AccessMixin, View):

  def dispatch(self, request, *args, **kwargs):
    self.check_has_manager_access()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, item_id):
    item = Item.all_objects.get(id=item_id)
    item.restore()
    return redirect("dashboard")
