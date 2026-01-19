from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from .models import Institution, Category
from .forms import InstitutionForm
from django.contrib.auth import get_user_model
from django.db import transaction
from user.models import Permission, Role


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
    context["institution"] = self.kwargs["id"]
    return context

def institution(request):
  return render(request, "pages/panel.html", {})


def autocomplete_categories_view(request):
  search = request.GET.get("search")
  limit = 20

  found_categories = Category.objects.filter(name__icontains=search)

  response = [
    {"name": categorie.name, "id": categorie.id} for categorie in found_categories
  ][:limit]

  return JsonResponse(response, safe=False)