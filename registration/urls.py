from django.urls import path
from .views import records, records_scan

urlpatterns = [
    path('registro/', records, name='records'),
    path('registro/escanear/', records_scan, name='records-scan'),
]
