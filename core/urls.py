from django.contrib import admin
from django.urls import path

from core.views import home, institution, patrimony, profile, patrimony_create, patrimony_edit, inventory_form, patrimony_detail, record_form, records, records_scan, user, user_detail, inventory, inventory_detail, login, signup, forgot_password, reset_password, new_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='dashboard'),
    path('instituicao/', institution, name='institution'),
    path('patrimonio/', patrimony, name='patrimony'),
    path('perfil/', profile, name='profile'),
    path('patrimonio/criar/', patrimony_create, name='patrimony-create'),
    path('patrimonio/<int:id>/editar/', patrimony_edit, name='patrimony-edit'),
    path('inventario/criar/', inventory_form, name='inventory-create'),
    path('patrimonio/<int:id>/', patrimony_detail, name='patrimony-detail'),
    path('patrimonio/<int:id>/registrar/', record_form, name='patrimony-register'),
    path('inventario/', inventory, name='inventory'),
    path('inventario/<int:id>/', inventory_detail, name='inventory-detail'),
    path('registro/', records, name='records'),
    path('registro/escanear/', records_scan, name='records-scan'),
    path('usuario/', user, name='users'),
    path('usuario/<int:id>/', user_detail, name='users-detail'),
    path('login/', login, name='signin'),
    path('criar-conta/', signup, name='signup'),
    path('esqueceu-senha/', forgot_password, name='forgot-password'),
    path('redefinir-senha/', reset_password, name='reset-password'),
    path('nova-senha/', new_password, name='new-password'),
]
