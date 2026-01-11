from django.urls import path, include
from .views import CreateInvetoryView, ListInventoryView, DetailInventoryView

urlpatterns = [
    path('', ListInventoryView.as_view(), name='inventory'),
    path('criar/', CreateInvetoryView.as_view(), name='inventory-create'),
    path('<int:inventory_id>/', DetailInventoryView.as_view(), name='inventory-detail'),
    path('<int:inventory_id>/registro/',include('registration.urls')),
]
