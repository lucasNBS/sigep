from django.urls import path
from .views import user, user_detail, login, signup, forgot_password, reset_password, new_password

urlpatterns = [
    path('usuario/', user, name='users'),
    path('usuario/<int:id>/', user_detail, name='users-detail'),
    path('login/', login, name='signin'),
    path('criar-conta/', signup, name='signup'),
    path('esqueceu-senha/', forgot_password, name='forgot-password'),
    path('redefinir-senha/', reset_password, name='reset-password'),
    path('nova-senha/', new_password, name='new-password'),
]