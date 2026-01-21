from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, View

from core.views import BaseContextView, AccessMixin
from registration.forms import RecordFilter

from .models import Item
from .forms import ItemForm, ItemFilter

class ListItemView(AccessMixin, BaseContextView, ListView):
  model = Item
  queryset = Item.all_objects
  template_name = "item/patrimony.html"

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

class RestoreItemView(AccessMixin, View):

  def dispatch(self, request, *args, **kwargs):
    self.check_has_manager_access()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, item_id):
    item = Item.all_objects.get(id=item_id)
    item.restore()
    return redirect("dashboard")
