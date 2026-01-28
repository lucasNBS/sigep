from django.urls import path
from .views import (
    DashboardView, SelectInstitutionView,
    UserListView, UserDetailView, PermissionUpdateView, ProfileUpdateView, PermissionRevokeView,
)

urlpatterns = [
    path("", UserListView.as_view(), name="permission-list"),
    path("<int:permission_id>/", UserDetailView.as_view(), name="permission-detail"),
    path("<int:permission_id>/editar/", PermissionUpdateView.as_view(), name="permission-edit"),
    path("<int:permission_id>/excluir/", PermissionRevokeView.as_view(), name="permission-delete"),

    path("perfil/", ProfileUpdateView.as_view(), name="profile"),
]
