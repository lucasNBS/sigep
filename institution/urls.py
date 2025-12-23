from django.urls import path
from .views import ListInstitutionsView

urlpatterns = [
    path('', ListInstitutionsView.as_view(), name='dashboard'),
]
