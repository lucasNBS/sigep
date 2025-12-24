from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from . import models, forms
from django.contrib.auth import get_user_model
from django.db import transaction
from user.models import Permission, Role


class ListInstitutionsView(ListView):
  model = models.Institution
  template_name = "institution/dashboard.html"
  context_object_name = "institutions"

  def get_queryset(self):
    user = self.request.user

    user_institutions = models.Institution.objects.filter(permissions__user=user)

    return user_institutions.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["form"] = forms.InstitutionForm()
    return context


class CreateInstitutionView(CreateView):
  model = models.Institution
  success_url = reverse_lazy("dashboard")
  form_class = forms.InstitutionForm

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
  model = models.Institution
  pk_url_kwarg = "id"
  success_url = reverse_lazy("dashboard")


class UpdateInstitutionView(UpdateView):
  model = models.Institution
  success_url = reverse_lazy("dashboard")
  form_class = forms.InstitutionForm
  pk_url_kwarg = "id"


class DetailInstitutionView(DetailView):
  model = models.Institution
  template_name = "institution/panel.html"
  pk_url_kwarg = "id"