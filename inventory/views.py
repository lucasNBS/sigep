from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, View
from .models import Inventory, Room
from .forms import  InventoryForm, InventoryFilter
from .choices import Status
from user.models import User, Permission
from institution.models import Institution
from item.models import Item
from registration.models import Record

class ListInventoryView(ListView):
  model = Inventory
  template_name = "inventory/inventory.html"
  context_object_name = "inventories"
  pk_url_kwarg = "institution_id"

  def get_paginate_by(self, queryset):
    page_size = self.request.GET.get("size")
    if page_size:
      return page_size
    return 10

  def get_queryset(self):
    queryset = Inventory.objects.select_related(
      "institution", "responsible", "leader_consultor"
    ).prefetch_related("consultors")

    self.filterset = InventoryFilter(self.request.GET, queryset=queryset)
    return self.filterset.qs.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10
    context["institution"] = self.kwargs["institution_id"]
    context["filter"] = self.filterset
    return context

  
class CreateInvetoryView(CreateView):
  model = Inventory
  template_name = "inventory/inventory-form.html"
  form_class = InventoryForm

  def get_success_url(self):
    return reverse_lazy(
      "inventory",
      kwargs={"institution_id": self.kwargs["institution_id"]}
    )

  def form_valid(self, form):
    form.instance.start_date = timezone.now()
    form.instance.institution = get_object_or_404(Institution, id = self.kwargs["institution_id"])
    inventory = form.save()
    inventory.responsible = self.request.user
    
    inventory.save()
    return super().form_valid(form)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["form"] = InventoryForm()
    context["institution"] = self.kwargs["institution_id"]
    return context


class DetailInventoryView(DetailView):
  model = Inventory
  template_name = "inventory/inventory-detail.html"
  pk_url_kwarg = "id"
  context_object_name = "inventory"


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user

    inventory = context["inventory"]

    items = Item.objects.filter(
        room__inventories=inventory
    ).count()

    items_records = Record.objects.filter(
        inventory=inventory
    ).values("item").distinct().count()



    institution = inventory.institution
    context["total_items"] = items
    context["items_records"] = items_records
    context["items_pendent"] = items - items_records
    context["percentage"] = f"{items_records/items:.0%}"
    context["role"] = get_object_or_404(Permission, institution=institution, user = user).role
    context["rooms"] = Room.objects.filter(inventories__institution=institution).distinct()
    context["institution"] = self.kwargs["institution_id"]
    context["inventory_id"] = self.kwargs["id"]
    return context

class UpdateInventoryView(UpdateView):
  model = Inventory
  form_class = InventoryForm
  pk_url_kwarg = "id"
  template_name="inventory/inventory-form.html"

  def get_success_url(self):
    return reverse_lazy(
      "inventory-detail",
      kwargs={"institution_id": self.kwargs["institution_id"],
              "id": self.kwargs["id"]}
      )

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["institution"] = self.kwargs["institution_id"]
    context["inventory_id"] = self.kwargs["id"]
    return context

class ConcludeInventoryView(View):
  def post(self, request, *args, **kwargs):
    inventory = get_object_or_404(Inventory, id = self.kwargs["id"])

    if inventory.status == Status.OPEN:
      inventory.status = Status.CLOSED
    elif inventory.status == Status.CLOSED:
      inventory.status = Status.OPEN
          
    inventory.save()

    return redirect(
      "inventory-detail",
      institution_id=kwargs["institution_id"],
      id=kwargs["id"],
    )

def autocomplete_rooms_view(request):
  search = request.GET.get("search")
  limit = 20

  found_rooms = Room.objects.filter(name__icontains=search)

  response = [
    {"name": room.name, "id": room.id} for room in found_rooms
  ][:limit]

  return JsonResponse(response, safe=False)