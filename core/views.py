from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic.base import ContextMixin

from institution.models import Institution
from user.models import Permission, Role


class BaseContextView(ContextMixin):

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    institution = Institution.objects.get(id=self.kwargs.get('institution_id'))
    user_permission = Permission.objects.get(user=self.request.user, institution=institution)
    context["permission"] = user_permission
    context["institution"] = institution
    return context
  

class AccessMixin:

  def get_institution(self):
    return Institution.objects.get(id=self.kwargs.get('institution_id'))
  
  def get_permission(self):
    user = self.request.user
    if not user.is_authenticated:
      raise PermissionDenied("Você não tem permissão para realizar esta ação")

    try:
      return Permission.objects.get(user=self.request.user, institution=self.get_institution())
    except:
      raise PermissionDenied("Você não tem permissão para realizar esta ação")
    
  def check_has_admin_access(self):
    role = self.get_permission().role
    if role not in [Role.ADMIN.value]:
      raise PermissionDenied("Você não tem autorização para realizar esta ação")
  
  def check_has_manager_access(self):
    role = self.get_permission().role
    if role not in [Role.ADMIN.value, Role.MANAGER.value]:
      raise PermissionDenied("Você não tem autorização para realizar esta ação")
  
  def check_has_user_access(self):
    role = self.get_permission().role
    if role not in [Role.ADMIN.value, Role.MANAGER.value, Role.USER.value]:
      raise PermissionDenied("Você não tem autorização para realizar esta ação")


def profile(request):
  return render(request, "pages/profile.html", {})
