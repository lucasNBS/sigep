from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import ListInstitutionsView, CreateInstitutionView, DeleteInstitutionView, UpdateInstitutionView, DetailInstitutionView

urlpatterns = [
    path('', ListInstitutionsView.as_view(), name='dashboard'),
    path('instituicao/criar/', CreateInstitutionView.as_view(), name='criar_instituicao'),
    path('instituicao/<int:id>/excluir/', DeleteInstitutionView.as_view(), name='excluir_instituicao'),
    path('instituicao/<int:id>/editar/', UpdateInstitutionView.as_view(), name='editar_instituicao'),
    path('institution/<int:id>/', DetailInstitutionView.as_view(), name='detalhar_instituicao'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
