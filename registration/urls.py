from django.urls import path
from .views import records_scan, CreateRecordView, RegisterSerialView

urlpatterns = [
    path('escanear/', records_scan, name='registration-scan'),
    path('serial/', RegisterSerialView.as_view(),name='registration-serial'),
    path('<str:registration_id>/', CreateRecordView.as_view(), name='registration-create'),
]
