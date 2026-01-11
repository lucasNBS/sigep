from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import profile
from registration.views import ListRecordsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('institution.urls')),
    path('', include('user.urls')),
    path('patrimonio/', include('item.urls')),
    path('perfil/', profile, name='profile'),
    path('dashboard/<int:institution_id>/inventario/', include('inventory.urls')),
    path('dashboard/<int:institution_id>/registro/', ListRecordsView.as_view(), name='records'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
