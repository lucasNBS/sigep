from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from django.db.models import Count, F

from .models import Institution
from .forms import InstitutionForm
from inventory.models import Inventory
from item.models import Item
from registration.models import Record
from django.contrib.auth import get_user_model
from django.db import transaction
from user.models import Permission, Role
from registration.choices import ConservationState
from item.choices import Status


class ListInstitutionsView(ListView):
  model = Institution
  template_name = "institution/dashboard.html"
  context_object_name = "institutions"
  form_class = InstitutionForm

  def get_queryset(self):
    user = self.request.user

    user_institutions = Institution.objects.filter(permissions__user=user)

    return user_institutions.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["form"] = InstitutionForm()
    return context


class CreateInstitutionView(CreateView):
  model = Institution
  success_url = reverse_lazy("dashboard")
  form_class = InstitutionForm

  def form_valid(self, form):
    user = self.request.user

    if not user.is_authenticated:
      form.add_error(None, "Usuário não autenticado.")
      return self.form_invalid(form)

    with transaction.atomic():
      institution = form.save()

      Permission.objects.create(
          user=user,
          institution=institution,
          role=Role.ADMIN.value, 
      )

    return super().form_valid(form)


class DeleteInstitutionView(DeleteView):
  model = Institution
  pk_url_kwarg = "id"
  success_url = reverse_lazy("dashboard")


class UpdateInstitutionView(UpdateView):
  model = Institution
  success_url = reverse_lazy("dashboard")
  form_class = InstitutionForm
  pk_url_kwarg = "id"


class DetailInstitutionView(DetailView):
  model = Institution
  template_name = "institution/panel.html"
  pk_url_kwarg = "id"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    institution_id = self.kwargs["id"]
    inventories = Inventory.objects.filter(institution__id=institution_id).annotate(
      total_items=Count("rooms__items",distinct=True),
      recorded_items=Count("records__item",distinct=True),
    ).annotate( pending_items=F("total_items") - F("recorded_items"))

    items_total = Item.objects.filter(institution__id=institution_id).count()

    records = Record.objects.filter(inventory__institution_id = institution_id, conservation_state__gt=ConservationState.POOR).count

    items_lost = Item.objects.filter(institution__id=institution_id, status=Status.LOST).count()

    context = super().get_context_data(**kwargs)
    context["records"] = records
    context["items_lost"] = items_lost
    context["items_total"] = items_total
    context["inventories"] = inventories
    context["institution"] = institution_id
    return context


def autocomplete_categories_view(request):
  search = request.GET.get("search")
  limit = 20

  found_categories = Category.objects.filter(name__icontains=search)

  response = [
    {"name": categorie.name, "id": categorie.id} for categorie in found_categories
  ][:limit]

  return JsonResponse(response, safe=False)