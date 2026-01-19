from django.urls import path
from .views import (
    SigninView, LogoutView, SignupView, DashboardView, SelectInstitutionView,
    UserListView, UserDetailView, PermissionUpdateView, ProfileUpdateView, PermissionRevokeView,
    ForgotPasswordView, ResetPasswordView, NewPasswordView
)

urlpatterns = [
    path("login/", SigninView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("criar-conta/", SignupView.as_view(), name="signup"),

    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("instituicao/selecionar/<int:institution_id>/", SelectInstitutionView.as_view(), name="select-institution"),

    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("redefinir-senha/", ResetPasswordView.as_view(), name="reset-password"),
    path("new-password/", NewPasswordView.as_view(), name="new-password"),

    path("usuario/", UserListView.as_view(), name="users"),
    path("usuario/<int:id>/", UserDetailView.as_view(), name="users-detail"),
    
    path("permissoes/<int:pk>/editar/", PermissionUpdateView.as_view(), name="permission_update"),
    path("permissoes/<int:pk>/remover/", PermissionRevokeView.as_view(), name="permission_remove"),

    
    path("perfil/", ProfileUpdateView.as_view(), name="profile"),
]
