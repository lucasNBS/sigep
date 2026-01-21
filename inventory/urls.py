from django.urls import path, include
from .views import CreateInvetoryView, ListInventoryView, DetailInventoryView, UpdateInventoryView, ConcludeInventoryView

urlpatterns = [
    path('', ListInventoryView.as_view(), name='inventory'),
    path('criar/', CreateInvetoryView.as_view(), name='inventory-create'),
    path('<int:inventory_id>/', DetailInventoryView.as_view(), name='inventory-detail'),
    path('<int:inventory_id>/registro/',include('registration.urls')),
    path('<int:id>/editar/', UpdateInventoryView.as_view(), name='inventory-edit'),
    path('<int:id>/concluir/', ConcludeInventoryView.as_view(), name='conclude-inventory'),
]
