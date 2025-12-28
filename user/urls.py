from django.urls import path
from .views import (
    UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView,
    login, signup, forgot_password, reset_password, new_password
)

urlpatterns = [
    path("usuario/", UserListView.as_view(), name="users"),
    path("usuario/novo/", UserCreateView.as_view(), name="users-create"),
    path("usuario/<int:id>/", UserDetailView.as_view(), name="users-detail"),
    path("usuario/<int:id>/editar/", UserUpdateView.as_view(), name="users-update"),
    path("usuario/<int:id>/deletar/", UserDeleteView.as_view(), name="users-delete"),

    path("login/", login, name="signin"),
    path("criar-conta/", signup, name="signup"),
    path("esqueceu-senha/", forgot_password, name="forgot-password"),
    path("redefinir-senha/", reset_password, name="reset-password"),
    path("nova-senha/", new_password, name="new-password"),
]
