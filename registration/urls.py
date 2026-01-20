from django.urls import path
from .views import records_scan, CreateRecordView, RegisterSerialView

urlpatterns = [
    path('escanear/', records_scan, name='records-scan'),
    path('serial/', RegisterSerialView.as_view(),name='register-serial'),
    path('<str:serial>/', CreateRecordView.as_view(), name='create-record'),
]
