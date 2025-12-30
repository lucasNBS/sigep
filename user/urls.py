from django.urls import path
from .views import (
    SigninView, LogoutView, SignupView,
    UserListView, UserDetailView, UserCreateView,
    UserUpdateView, UserDeleteView, ProfileUpdateView
)

from .views import forgot_password, reset_password, new_password

urlpatterns = [
    path("login/", SigninView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("criar-conta/", SignupView.as_view(), name="signup"),
    
    
    path("esqueceu-senha/", forgot_password, name="forgot-password"),
    path("redefinir-senha/", reset_password, name="reset-password"),
    path("nova-senha/", new_password, name="new-password"),

    path("usuario/", UserListView.as_view(), name="users"),
    path("usuario/novo/", UserCreateView.as_view(), name="users-create"),
    path("usuario/<int:id>/", UserDetailView.as_view(), name="users-detail"),
    path("usuario/<int:id>/editar/", UserUpdateView.as_view(), name="users-update"),
    path("usuario/<int:id>/deletar/", UserDeleteView.as_view(), name="users-delete"),
    path("perfil/", ProfileUpdateView.as_view(), name="profile"),
]
