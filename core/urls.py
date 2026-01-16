from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import profile

from institution.views import autocomplete_categories_view
from inventory.views import autocomplete_rooms_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('institution.urls')),
    path('', include('user.urls')),
    path('patrimonio/', include('item.urls')),
    path('perfil/', profile, name='profile'),
    path('dashboard/<int:institution_id>/inventario/', include('inventory.urls')),
    path('registro/', include('registration.urls')),
    path('salas/autocomplete/', autocomplete_rooms_view, name='rooms-autocomplete'),
    path('categorias/autocomplete/', autocomplete_categories_view, name='categories-autocomplete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
