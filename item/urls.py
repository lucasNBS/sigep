from django.urls import path
from .views import ListItemView, UpdateItemView, DetailItemView, CreateItemView, DeleteItemView, restore_item_view, record_form, DownloadItemSpreadSheetView

urlpatterns = [
    path('', ListItemView.as_view(), name='patrimony'),
    path('criar/', CreateItemView.as_view(), name='patrimony-create'),
    path('<int:id>/editar/', UpdateItemView.as_view(), name='patrimony-edit'),
    path('<int:id>/', DetailItemView.as_view(), name='patrimony-detail'),
    path('<int:id>/remover/', DeleteItemView.as_view(), name='patrimony-remove'),
    path('<int:id>/restaurar/', restore_item_view, name='patrimony-restore'),
    path('<int:id>/registrar/', record_form, name='patrimony-register'),
    path(
      'planilha/download/',
      DownloadItemSpreadSheetView.as_view(),
      name='patrimony-spreadsheet-download'
    ),
]
