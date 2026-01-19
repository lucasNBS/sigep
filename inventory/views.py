<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from . import models, forms
from user import models as user_models
from institution import models as inst_models
from registration.models import Record
from registration.forms import RegisterSerialForm, RecordFilter
=======
from django.http import JsonResponse
from django.shortcuts import render
>>>>>>> 3bc282dd34f67ea5347134174ec9450c932443be

from . import models

def inventory_form(request):
  return render(request, "pages/inventory-form.html", {})

def inventory(request):
  return render(request, "pages/inventory.html", {})

<<<<<<< HEAD
  def get_queryset(self):
    queryset = models.Inventory.objects.select_related(
      "institution", "responsible", "leader_consultor"
    ).prefetch_related("consultors")

    self.filterset = forms.InventoryFilter(self.request.GET, queryset=queryset)
    return self.filterset.qs.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10
    context["institution"] = self.kwargs["institution_id"]
    context["filter"] = self.filterset
    return context

  
class CreateInvetoryView(CreateView):
  model = models.Inventory
  template_name = "inventory/inventory-form.html"
  form_class = forms.InventoryForm

  def get_success_url(self):
    return reverse_lazy(
      "inventory-detail",
      kwargs={
        "institution_id": self.kwargs["institution_id"],
      }
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
  pk_url_kwarg = "inventory_id"
  context_object_name = "inventory"


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    institution = get_object_or_404(inst_models.Institution, id = self.kwargs["institution_id"])

    inventory = self.object
    records_qs = Record.objects.filter(inventory=inventory)
    filterset = RecordFilter(self.request.GET, queryset=records_qs)

    context["rooms"] = models.Room.objects.filter(inventories__institution=institution).distinct()
    context["institution"] = self.kwargs["institution_id"]
    context["inventory_id"] = self.kwargs["inventory_id"]
    context["records"] = filterset.qs.distinct
    context["form"] = RegisterSerialForm()
    context["filter"] = filterset
    return context

=======
def inventory_detail(request, id):
  return render(request, "pages/inventory-detail.html", {})

def autocomplete_rooms_view(request):
  search = request.GET.get("search")
  limit = 20

  found_rooms = models.Room.objects.filter(name__icontains=search)

  response = [
    {"name": room.name, "id": room.id} for room in found_rooms
  ][:limit]

  return JsonResponse(response, safe=False)
>>>>>>> 3bc282dd34f67ea5347134174ec9450c932443be
