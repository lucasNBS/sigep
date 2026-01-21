from django.urls import path
from .views import ListItemView, UpdateItemView, DetailItemView, CreateItemView, DeleteItemView, RestoreItemView

urlpatterns = [
    path('', ListItemView.as_view(), name='item-list'),
    path('criar/', CreateItemView.as_view(), name='item-create'),
    path('<str:item_id>/editar/', UpdateItemView.as_view(), name='item-edit'),
    path('<str:item_id>/', DetailItemView.as_view(), name='item-detail'),
    path('<str:item_id>/excluir/', DeleteItemView.as_view(), name='item-delete'),
    path('<str:item_id>/restaurar/', RestoreItemView.as_view(), name='item-restore'),
]
