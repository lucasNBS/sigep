from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from . import models, forms
from user import models as user_models


class ListInventoryView(ListView):
  model = models.Inventory
  template_name = "inventory/inventory.html"
  context_object_name = "inventories"

  def get_paginate_by(self, queryset):
    page_size = self.request.GET.get("size")
    if page_size:
      return page_size
    return 10

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10
    return context


class CreateInvetoryView(CreateView):
  model = models.Inventory
  template_name = "inventory/inventory-form.html"
  success_url = reverse_lazy("inventory")
  form_class = forms.InventoryForm

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs["user"] = self.request.user
    return kwargs

  def form_valid(self, form):
    inventory = form.save()
    inventory.responsible = self.request.user
    form.instance.start_date = timezone.now()
    inventory.save()
    return super().form_valid(form)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["form"] = forms.InventoryForm()
    return context

class DetailInventoryView(DetailView):
  model = models.Inventory
  template_name = "inventory/inventory-detail.html"
  pk_url_kwarg = "id"
  context_object_name = "inventory"


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    institution = context["inventory"].institution
    context["rooms"] = models.Room.objects.filter(inventories__institution=institution).distinct()
    return context