from django.urls import path
from .views import (
    SigninView, LogoutView, SignupView, DashboardView, SelectInstitutionView,
    UserListView, UserDetailView, UserCreateView, PermissionUpdateView, ProfileUpdateView, PermissionRevokeView,
    forgot_password, reset_password, new_password,
)

urlpatterns = [
    path("login/", SigninView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("criar-conta/", SignupView.as_view(), name="signup"),

    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("instituicao/selecionar/<int:institution_id>/", SelectInstitutionView.as_view(), name="select-institution"),

    path("esqueceu-senha/", forgot_password, name="forgot-password"),
    path("redefinir-senha/", reset_password, name="reset-password"),
    path("nova-senha/", new_password, name="new-password"),

    path("usuario/", UserListView.as_view(), name="users"),
    path("usuario/novo/", UserCreateView.as_view(), name="users-create"),
    path("usuario/<int:id>/", UserDetailView.as_view(), name="users-detail"),
    path("usuario/<int:id>/editar/", PermissionUpdateView.as_view(), name="users-update"),
    
    path("permissoes/<int:pk>/remover/", PermissionRevokeView.as_view(), name="permission_remove"),

    
    path("perfil/", ProfileUpdateView.as_view(), name="profile"),
]
