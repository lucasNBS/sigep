from django.urls import path
from .views import ListItemView, UpdateItemView, DetailItemView, CreateItemView, DeleteItemView, restore_item_view, DownloadItemSpreadSheetView

urlpatterns = [
    path('', ListItemView.as_view(), name='patrimony'),
    path('criar/', CreateItemView.as_view(), name='patrimony-create'),
    path('<str:id>/editar/', UpdateItemView.as_view(), name='patrimony-edit'),
    path('<str:id>/', DetailItemView.as_view(), name='patrimony-detail'),
    path('<str:id>/remover/', DeleteItemView.as_view(), name='patrimony-remove'),
    path('<str:id>/restaurar/', restore_item_view, name='patrimony-restore'),
    path(
      'planilha/download/',
      DownloadItemSpreadSheetView.as_view(),
      name='patrimony-spreadsheet-download'
    ),
]
