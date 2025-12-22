from django.contrib import admin
from django.urls import path, include

from core.views import home, profile

from institution.views import autocomplete_categories_view
from inventory.views import autocomplete_rooms_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='dashboard'),
    path('', include('user.urls')),
    path('patrimonio/', include('item.urls')),
    path('perfil/', profile, name='profile'),
    path('inventario/', include('inventory.urls')),
    path('instituicao/', include('institution.urls')),
    path('registro/', include('registration.urls')),
    path('salas/autocomplete/', autocomplete_rooms_view, name='rooms-autocomplete'),
    path('categorias/autocomplete/', autocomplete_categories_view, name='categories-autocomplete'),
]
