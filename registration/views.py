from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, View

from core.views import BaseContextView, AccessMixin
from item.models import Item
from institution.models import Institution
from inventory.models import Inventory

from .models import Record
from .forms import RecordForm, RecordFilter


class ListRecordsView(AccessMixin, BaseContextView, ListView):
  model = Record
  template_name = "registration/record.html"
  context_object_name = "records"
  pk_url_kwarg = "institution_id"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_user_access()
    return super().dispatch(request, *args, **kwargs)

  def get_paginate_by(self, queryset):
    page_size = self.request.GET.get("size")
    if page_size:
      return page_size
    return 10

  def get_queryset(self):
    queryset = Record.objects.select_related("item", "user").prefetch_related("item__room")

    self.filterset = RecordFilter(self.request.GET, queryset=queryset)
    return self.filterset.qs.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10
    context["filter"] = self.filterset
    return context

def records_scan(request, institution_id, inventory_id):
  return render(request, "pages/record-scan.html", {})

class RegisterSerialView(View):
  def post(self, request, *args, **kwargs):
    serial = request.POST.get("serial")

    if not serial:
      return redirect(request.META.get("HTTP_REFERER", "/"))

    return redirect(
      "registration-create",
      institution_id=kwargs["institution_id"],
      inventory_id=kwargs["inventory_id"],
      serial=serial
    )

class CreateRecordView(CreateView):
  model = Record
  template_name = "registration/record-form.html"
  slug_field = "serial"
  slug_url_kwarg = "serial"
  form_class = RecordForm
  
  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs["institution"] = get_object_or_404(Institution, id=self.kwargs["institution_id"])
    return kwargs

  def get_success_url(self):
    return reverse_lazy(
      "inventory-detail",
      kwargs={
        "institution_id": self.kwargs["institution_id"],
        "inventory_id": self.kwargs["inventory_id"]
      }
    )
 
  def form_valid(self, form):
    form.instance.inventory = get_object_or_404(Inventory, id = self.kwargs["inventory_id"])
    form.instance.item = get_object_or_404(Item, serial=self.kwargs["serial"], institution_id=self.kwargs["institution_id"])
    record = form.save()
    record.recorded_at = timezone.now()
    
    record.user = self.request.user
    
    record.save() 

    room = form.cleaned_data.get("room")
    if room:
      item = record.item
      item.room = room
      item.save(update_fields=["room"])

    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["institution"] = self.kwargs["institution_id"]
    context["item"] = get_object_or_404(Item, serial=self.kwargs["serial"], institution_id=self.kwargs["institution_id"],)
    return context

