from django.urls import path
from .views import ScanRecordView, RegisterSerialView

urlpatterns = [
    path('escanear/', ScanRecordView.as_view(), name='registration-scan'),
    path('serial/', RegisterSerialView.as_view(),name='registration-serial'),
]
