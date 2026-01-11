from django.urls import path
from .views import patrimony, patrimony_create, patrimony_edit, patrimony_detail

urlpatterns = [
    path('', patrimony, name='patrimony'),
    path('criar/', patrimony_create, name='patrimony-create'),
    path('<int:id>/editar/', patrimony_edit, name='patrimony-edit'),
    path('<int:id>/', patrimony_detail, name='patrimony-detail'),
]
