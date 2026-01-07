from django.contrib import admin
from django.urls import path, include

from core.views import home, profile

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='dashboard'),
    path('', include('user.urls')),
    path('patrimonio/', include('item.urls')),
    path('perfil/', profile, name='profile'),
    path('inventario/', include('inventory.urls')),
    path('instituicao/', include('institution.urls')),
    path('registro/', include('registration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
