from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from . import models, forms

# remover quando o login estiver implementado
from user import models as usermodel

class ListInstitutionsView(ListView):
  model = models.Institution
  template_name = "institution/dashboard.html"
  context_object_name = "institutions"

  def get_queryset(self):
    user = self.request.user

    # remover quando o login estiver implementado
    if not user.is_authenticated:
      user = usermodel.User.objects.first()

    user_institutions = models.Institution.objects.filter(permissions__user=user)

    return user_institutions.distinct()
