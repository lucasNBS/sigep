from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from . import models, forms
from user import models as user_models
from institution import models as inst_models

class ListInventoryView(ListView):
  model = models.Inventory
  template_name = "inventory/inventory.html"
  context_object_name = "inventories"
  pk_url_kwarg = "institution_id"

  def get_paginate_by(self, queryset):
    page_size = self.request.GET.get("size")
    if page_size:
      return page_size
    return 10

  def get_queryset(self):
    qs = models.Inventory.objects.select_related(
      "institution", "responsible", "leader_consultor"
    ).prefetch_related("consultors")

    self.form = forms.InventoryFilterForm(self.request.GET or None)

    if self.form.is_valid():
      form_data = self.form.cleaned_data

      if form_data.get("title"):
        qs = qs.filter(title__icontains=form_data["title"])

      if form_data.get("responsible"):
        qs = qs.filter(responsible=form_data["responsible"])

      if form_data.get("leader_consultor"):
        qs = qs.filter(leader_consultor=form_data["leader_consultor"])

      if form_data.get("consultor"):
        qs = qs.filter(consultors=form_data["consultor"])

      if form_data.get("status"):
        qs = qs.filter(status=form_data["status"])

      if form_data.get("date_start"):
        qs = qs.filter(start_date__date__gte=form_data["date_start"])

      if form_data.get("date_end"):
        qs = qs.filter(start_date__date__lte=form_data["date_end"])

    return qs.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10
    context["institution"] = self.kwargs["institution_id"]
    context["filter_form"] = self.form
    return context

  
class CreateInvetoryView(CreateView):
  model = models.Inventory
  template_name = "inventory/inventory-form.html"
  form_class = forms.InventoryForm

  def get_success_url(self):
    return reverse_lazy(
      "inventory",
      kwargs={"institution_id": self.kwargs["institution_id"]}
    )

  def form_valid(self, form):
    form.instance.start_date = timezone.now()
    form.instance.institution = get_object_or_404(inst_models.Institution, id = self.kwargs["institution_id"])
    inventory = form.save()
    inventory.responsible = self.request.user
    
    inventory.save()
    return super().form_valid(form)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["form"] = forms.InventoryForm()
    context["institution"] = self.kwargs["institution_id"]
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
    context["institution"] = self.kwargs["institution_id"]
    return context