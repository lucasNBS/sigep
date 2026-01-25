from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F

from core.views import BaseContextView, AccessMixin
from inventory.models import Inventory
from item.choices import Status
from item.models import Item
from registration.choices import ConservationState
from registration.models import Record
from user.models import Permission, Role

from .models import Institution, Category
from .forms import InstitutionForm


class ListInstitutionsView(LoginRequiredMixin, ListView):
  login_url = reverse_lazy("signin")
  redirect_field_name = "next"
  model = Institution
  template_name = "pages/dashboard.html"
  form_class = InstitutionForm

  def get_queryset(self):
    permissions = Permission.objects.filter(user=self.request.user).values_list("institution__id")
    return self.model.objects.filter(id__in=permissions)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["user"] = self.request.user
    context["form"] = InstitutionForm()
    context["institutions"] = [
      {
        "item": item,
        "form": InstitutionForm(instance=item)
      }
      for item in context["object_list"]
    ]
    return context


class CreateInstitutionView(LoginRequiredMixin, CreateView):
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


class DeleteInstitutionView(AccessMixin, DeleteView):
  model = Institution
  success_url = reverse_lazy("dashboard")
  pk_url_kwarg = "institution_id"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_admin_access()
    return super().dispatch(request, *args, **kwargs)

class UpdateInstitutionView(AccessMixin, UpdateView):
  model = Institution
  success_url = reverse_lazy("dashboard")
  form_class = InstitutionForm
  pk_url_kwarg = "institution_id"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_admin_access()
    return super().dispatch(request, *args, **kwargs)


class DetailInstitutionView(AccessMixin, BaseContextView, DetailView):
  model = Institution
  template_name = "institution/panel.html"
  pk_url_kwarg = "institution_id"

  def dispatch(self, request, *args, **kwargs):
    self.check_has_manager_access()
    if self.has_user_access():
      return redirect(reverse(
        'registration-list', kwargs={'institution_id': self.kwargs["institution_id"]}
      ))
    return super().dispatch(request, *args, **kwargs)

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
    return context


class AutocompleteCategoriesView(AccessMixin, View):

  def dispatch(self, request, *args, **kwargs):
    self.check_has_user_access()
    return super().dispatch(request, *args, **kwargs)

  def get(self, request, institution_id):
    search = request.GET.get("search")
    limit = 20

    found_categories = Category.objects.filter(name__icontains=search)

    response = [
      {"name": categorie.name, "id": categorie.id} for categorie in found_categories
    ][:limit]

    return JsonResponse(response, safe=False)
