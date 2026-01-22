from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, View, TemplateView

from core.views import BaseContextView, AccessMixin
from item.models import Item
from institution.models import Institution
from inventory.choices import Status
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

class ScanRecordView(AccessMixin, BaseContextView, TemplateView):
  template_name = "pages/record-scan.html"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_user_access()
    request.session["inventory_id"] = self.kwargs["inventory_id"]
    return super().dispatch(request, *args, **kwargs)

class RegisterSerialView(AccessMixin, View):

  def dispatch(self, request, *args, **kwargs):
    self.check_has_user_access()
    request.session["inventory_id"] = self.kwargs["inventory_id"]
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    serial = request.POST.get("serial")

    if not serial:
      return redirect(request.META.get("HTTP_REFERER", "/"))
    
    item = get_object_or_404(Item, serial=serial, institution__id=kwargs["institution_id"])

    return redirect(
      "item-registration",
      institution_id=kwargs["institution_id"],
      item_id=item.id,
    )

class CreateRecordView(AccessMixin, BaseContextView, CreateView):
  model = Record
  template_name = "registration/record-form.html"
  form_class = RecordForm

  def dispatch(self, request, *args, **kwargs):
    self.check_has_user_access()

    user_has_access_to_inventory = Inventory.objects.filter(
      Q(leader_consultor=self.request.user) | Q(consultors=self.request.user),
      id=self.request.session.get("inventory_id")
    ).distinct().exists()

    item = get_object_or_404(Item, id=self.kwargs["item_id"])

    item_belongs_to_inventory = Inventory.objects.filter(
      id=self.request.session.get("inventory_id"), rooms=item.room
    ).exists()

    invenvtory_is_open = Inventory.objects.filter(
      id=self.request.session.get("inventory_id"), rooms=item.room, status=Status.OPEN
    ).exists()

    if not invenvtory_is_open:
      raise PermissionError("Este inventário foi encerrado")

    if not item_belongs_to_inventory:
      raise PermissionError("Este item não faz parte deste inventário")

    if not user_has_access_to_inventory:
      raise PermissionError("Você não tem autorização para realizar esta ação")

    return super().dispatch(request, *args, **kwargs)
  
  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs["institution"] = get_object_or_404(Institution, id=self.kwargs["institution_id"])
    return kwargs

  def get_success_url(self):
    return reverse_lazy(
      "inventory-detail",
      kwargs={
        "institution_id": self.kwargs["institution_id"],
        "inventory_id": self.request.session.get("inventory_id")
      }
    )
 
  def form_valid(self, form):
    form.instance.inventory = get_object_or_404(
      Inventory, id=self.request.session.get("inventory_id")
    )
    form.instance.item = get_object_or_404(Item, id=self.kwargs["item_id"])
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
    context["item"] = get_object_or_404(Item, id=self.kwargs["item_id"])
    return context
