from django.urls import path
from .views import patrimony, patrimony_create, patrimony_edit, patrimony_detail, record_form

urlpatterns = [
    path('patrimonio/', patrimony, name='patrimony'),
    path('patrimonio/criar/', patrimony_create, name='patrimony-create'),
    path('patrimonio/<int:id>/editar/', patrimony_edit, name='patrimony-edit'),
    path('patrimonio/<int:id>/', patrimony_detail, name='patrimony-detail'),
    path('patrimonio/<int:id>/registrar/', record_form, name='patrimony-register'),
]
