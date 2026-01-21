from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View

from core.views import BaseContextView, AccessMixin
from institution.models import Institution
from registration.forms import RecordFilter, RegisterSerialForm
from registration.models import Record

from .models import Inventory, Room
from .forms import  InventoryForm, InventoryFilter
from .choices import Status


class ListInventoryView(AccessMixin, BaseContextView, ListView):
  model = Inventory
  template_name = "inventory/inventory.html"
  context_object_name = "inventories"
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
    queryset = Inventory.objects.filter(
      Q(leader_consultor=self.request.user) | Q(consultors=self.request.user)
    ).distinct().select_related("institution", "responsible", "leader_consultor").prefetch_related(
      "consultors"
    )

    self.filterset = InventoryFilter(self.request.GET, queryset=queryset)

    return self.filterset.qs.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10
    context["filter"] = self.filterset
    return context

  
class CreateInvetoryView(AccessMixin, BaseContextView, CreateView):
  model = Inventory
  template_name = "inventory/inventory-form.html"
  form_class = InventoryForm
  title = "Abrir Processo de Inventário"
  button = "Abrir Inventário"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_manager_access()
    return super().dispatch(request, *args, **kwargs)

  def get_success_url(self):
    return reverse(
      "inventory-list",
      kwargs={"institution_id": self.kwargs["institution_id"]}
    )

  def get_form_kwargs(self):
    form_kwargs = super().get_form_kwargs()
    form_kwargs["institution_id"] = self.kwargs.get('institution_id')
    form_kwargs["user_id"] = self.request.user.id
    return form_kwargs

  def form_valid(self, form):
    form.instance.start_date = timezone.now()
    form.instance.institution = get_object_or_404(Institution, id = self.kwargs["institution_id"])
    inventory = form.save()
    inventory.responsible = self.request.user
    
    inventory.save()
    return super().form_valid(form)


class DetailInventoryView(AccessMixin, BaseContextView, DetailView):
  model = Inventory
  template_name = "inventory/inventory-detail.html"
  pk_url_kwarg = "inventory_id"
  context_object_name = "inventory"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_user_access()
    return super().dispatch(request, *args, **kwargs)

  def get_queryset(self, *args, **kwargs):
    return Inventory.objects.filter(
      Q(leader_consultor=self.request.user) | Q(consultors=self.request.user)
    ).distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10

    records_qs = Record.objects.filter(inventory=self.object)
    filterset = RecordFilter(self.request.GET, queryset=records_qs)
    paginator = Paginator(filterset.qs, context["size"])
    page_number = self.request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context["page_obj"] = page_obj
    context["records"] = page_obj.object_list
    context["form"] = RegisterSerialForm()
    context["filter"] = filterset
    context["rooms"] = self.object.rooms.all()
    return context

class UpdateInventoryView(AccessMixin, BaseContextView, UpdateView):
  model = Inventory
  form_class = InventoryForm
  pk_url_kwarg = "inventory_id"
  template_name="inventory/inventory-form.html"
  title = "Editar Processo de Inventário"
  button = "Editar Inventário"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_manager_access()
    return super().dispatch(request, *args, **kwargs)

  def get_success_url(self):
    return reverse_lazy(
        "inventory-detail",
        kwargs={
          "institution_id": self.kwargs["institution_id"],
          "inventory_id": self.kwargs["inventory_id"]
        }
      )

  def get_form_kwargs(self):
    form_kwargs = super().get_form_kwargs()
    form_kwargs["institution_id"] = self.kwargs.get('institution_id')
    form_kwargs["user_id"] = self.request.user.id
    return form_kwargs


class ConcludeInventoryView(AccessMixin, View):

  def dispatch(self, request, *args, **kwargs):
    self.check_has_user_access()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    inventory = get_object_or_404(
      Inventory, id=self.kwargs["inventory_id"], leader_consultor=self.request.user
    )

    if inventory.status == Status.OPEN:
      inventory.status = Status.CLOSED
    elif inventory.status == Status.CLOSED:
      inventory.status = Status.OPEN

    inventory.save()

    return redirect(
      "inventory-detail",
      institution_id=kwargs["institution_id"],
      inventory_id=kwargs["inventory_id"],
    )
  

class AutocompleteRoomsView(AccessMixin, View):

  def dispatch(self, request, *args, **kwargs):
    self.check_has_user_access()
    return super().dispatch(request, *args, **kwargs)

  def get(self, request, institution_id):
    search = request.GET.get("search")
    limit = 20

    found_rooms = Room.objects.filter(name__icontains=search)

    response = [
      {"name": room.name, "id": room.id} for room in found_rooms
    ][:limit]


    return JsonResponse(response, safe=False)
