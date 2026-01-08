from django.urls import path
from .views import ListRecordsView, records_scan

urlpatterns = [
    path('', ListRecordsView.as_view(), name='records'),
    path('escanear/', records_scan, name='records-scan'),
]
