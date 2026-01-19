from django.urls import path
from .views import records, records_scan

urlpatterns = [
    path('/', records, name='records'),
    path('escanear/', records_scan, name='records-scan'),
]
