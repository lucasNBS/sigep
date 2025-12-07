from django.urls import path
from .views import inventory_form, inventory, inventory_detail

urlpatterns = [
    path('', inventory, name='inventory'),
    path('criar/', inventory_form, name='inventory-create'),
    path('<int:id>/', inventory_detail, name='inventory-detail'),
]
