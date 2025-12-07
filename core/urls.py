from django.contrib import admin
from django.urls import path, include

from core.views import home, institution, patrimony, profile, patrimony_create, patrimony_edit, inventory_form, patrimony_detail, record_form, records, records_scan, inventory, inventory_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='dashboard'),
    path('', include('user.urls')),
    path('perfil/', profile, name='profile'),
    path('instituicao/', institution, name='institution'),
    path('patrimonio/', patrimony, name='patrimony'),
    path('patrimonio/criar/', patrimony_create, name='patrimony-create'),
    path('patrimonio/<int:id>/editar/', patrimony_edit, name='patrimony-edit'),
    path('patrimonio/<int:id>/', patrimony_detail, name='patrimony-detail'),
    path('patrimonio/<int:id>/registrar/', record_form, name='patrimony-register'),
    path('inventario/criar/', inventory_form, name='inventory-create'),
    path('inventario/', inventory, name='inventory'),
    path('inventario/<int:id>/', inventory_detail, name='inventory-detail'),
    path('registro/', records, name='records'),
    path('registro/escanear/', records_scan, name='records-scan'),
]
