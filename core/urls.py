from django.contrib import admin
from django.urls import path, include

from core.views import home, profile, records, records_scan

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='dashboard'),
    path('', include('user.urls')),
    path('perfil/', profile, name='profile'),
    path('inventario/', include('inventory.urls')),
    path('instituicao/', include('institution.urls')),
    path('registro/', records, name='records'),
    path('registro/escanear/', records_scan, name='records-scan'),
]
