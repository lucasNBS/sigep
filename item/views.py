from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

from .models import Item
from .forms import ItemForm, ItemFilter

class ListItemView(ListView):
  model = Item
  queryset = Item.all_objects
  template_name = "item/patrimony.html"

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

def restore_item_view(request, id):
  item = Item.all_objects.get(id=id)
  item.restore()
  return redirect("dashboard")

def record_form(request, id):
  return render(request, "pages/record-form.html", {})
