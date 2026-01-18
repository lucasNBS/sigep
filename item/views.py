import pandas as pd

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, View
from django.views.generic.edit import FormMixin

from core.settings import MAX_ERRORS
from core.utils import handle_selected_element, validate_dataframe_column
from institution.models import Institution, Category
from inventory.models import Room

from .models import Item
from .forms import ItemForm, ItemFilter, ItemImport


class ListItemView(FormMixin, ListView):
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

class CreateItemView(CreateView):
  model = Item
  template_name = "item/patrimony-form.html"
  success_url = reverse_lazy("dashboard")
  form_class = ItemForm

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = "Cadastrar Item"
    return context
  
class UpdateItemView(UpdateView):
  model = Item
  pk_url_kwarg = "id"
  queryset = Item.all_objects
  template_name = "item/patrimony-form.html"
  success_url = reverse_lazy("dashboard")
  form_class = ItemForm

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = "Editar Item"
    return context

class DetailItemView(DetailView):
  model = Item
  pk_url_kwarg = "id"
  queryset = Item.all_objects
  template_name = "item/patrimony-detail.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10
    return context

class DeleteItemView(DeleteView):
  model = Item
  pk_url_kwarg = "id"
  template_name = "item/confirm-delete.html"
  success_url = reverse_lazy("dashboard")

class DownloadItemSpreadSheetView(View):
  filepath = "static/media/PlanilhaItem.ods"
  filename = "PlanilhaItem.ods"

  def get(self, request, *args, **kwargs):
    with open(self.filepath, "rb") as f:
      file = f.read()

    response = HttpResponse(file, content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = f"attachment; filename={self.filename}"

    return response

def restore_item_view(request, id):
  item = Item.all_objects.get(id=id)
  item.restore()
  return redirect("dashboard")

def record_form(request, id):
  return render(request, "pages/record-form.html", {})
