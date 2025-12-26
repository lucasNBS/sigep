from django.contrib import admin
from django.urls import path, include

from core.views import home, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('institution.urls')),
    path('', include('user.urls')),
    path('patrimonio/', include('item.urls')),
    path('perfil/', profile, name='profile'),
    path('dashboard/<int:institution_id>/inventario/', include('inventory.urls')),
    path('registro/', include('registration.urls')),
]
