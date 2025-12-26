from django.urls import path
from .views import CreateInvetoryView, ListInventoryView, DetailInventoryView

urlpatterns = [
    path('', ListInventoryView.as_view(), name='inventory'),
    path('criar/', CreateInvetoryView.as_view(), name='inventory-create'),
    path('<int:id>/', DetailInventoryView.as_view(), name='inventory-detail'),
]
