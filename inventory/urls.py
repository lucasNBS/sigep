from django.urls import path
from .views import CreateInvetoryView, ListInventoryView, DetailInventoryView, UpdateInventoryView, ConcludeInventoryView

urlpatterns = [
    path('', ListInventoryView.as_view(), name='inventory'),
    path('criar/', CreateInvetoryView.as_view(), name='inventory-create'),
    path('<int:id>/', DetailInventoryView.as_view(), name='inventory-detail'),
    path('<int:id>/editar/', UpdateInventoryView.as_view(), name='inventory-edit'),
    path('<int:id>/concluir/', ConcludeInventoryView.as_view(), name='conclude-inventory'),
]
