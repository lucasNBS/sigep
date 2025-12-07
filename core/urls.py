from django.contrib import admin
from django.urls import path, include

from core.views import home, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='dashboard'),
    path('', include('user.urls')),
    path('sala/', include('room.urls')),
    path('patrimonio/', include('item.urls')),
    path('perfil/', profile, name='profile'),
    path('inventario/', include('inventory.urls')),
    path('instituicao/', include('institution.urls')),
    path('registro/', include('registration.urls')),
]
