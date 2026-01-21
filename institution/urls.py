from django.urls import path, include

from institution.views import AutocompleteCategoriesView
from inventory.views import AutocompleteRoomsView
from registration.views import ListRecordsView

from .views import CreateInstitutionView, DeleteInstitutionView, UpdateInstitutionView, DetailInstitutionView


urlpatterns = [
    path('criar/', CreateInstitutionView.as_view(), name='institution-create'),
    path(
      '<int:institution_id>/excluir/', DeleteInstitutionView.as_view(), name='institution-delete'
    ),
    path('<int:institution_id>/editar/', UpdateInstitutionView.as_view(), name='institution-edit'),
    path('<int:institution_id>/', DetailInstitutionView.as_view(), name='institution-detail'),
    path('<int:institution_id>/patrimonio/', include('item.urls')),
    path('<int:institution_id>/inventario/', include('inventory.urls')),
    path('<int:institution_id>/permissao/', include('user.urls')),
    path('<int:institution_id>/registro/', ListRecordsView.as_view(),name='registration-list'),
    path(
      '<int:institution_id>/sala/autocomplete/',
      AutocompleteRoomsView.as_view(),
      name='room-autocomplete'
    ),
    path(
      '<int:institution_id>/categoria/autocomplete/',
      AutocompleteCategoriesView.as_view(),
      name='categorie-autocomplete'
    ),
] 
