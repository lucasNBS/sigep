from django.urls import path

from registration.views import CreateRecordView

from .views import ListItemView, UpdateItemView, DetailItemView, CreateItemView, DeleteItemView, RestoreItemView, DownloadItemSpreadSheetView

urlpatterns = [
    path('', ListItemView.as_view(), name='item-list'),
    path('criar/', CreateItemView.as_view(), name='item-create'),
    path('<str:item_id>/editar/', UpdateItemView.as_view(), name='item-edit'),
    path('<str:item_id>/', DetailItemView.as_view(), name='item-detail'),
    path('<str:item_id>/excluir/', DeleteItemView.as_view(), name='item-delete'),
    path('<str:item_id>/restaurar/', RestoreItemView.as_view(), name='item-restore'),
    path('<str:item_id>/registrar/', CreateRecordView.as_view(), name='item-registration'),
    path(
      'planilha/download/',
      DownloadItemSpreadSheetView.as_view(),
      name='item-spreadsheet-download'
    ),
]
