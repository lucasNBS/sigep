from django.contrib import admin
from django.urls import path

from core.views import home, patrimony, profile, patrimony_form, inventory_form, patrimony_detail, record_form, records, user, inventory, inventory_detail, login, signup, forgot_password, reset_password, new_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('patrimonio/', patrimony, name='patrimony'),
    path('perfil/', profile, name='profile'),
    path('patrimonio/criar/', patrimony_form, name='patrimony-create'),
    path('inventario/criar/', inventory_form, name='inventory-create'),
    path('patrimonio/<int:id>/', patrimony_detail, name='patrimony-detail'),
    path('patrimonio/<int:id>/registrar/', record_form, name='patrimonio-register'),
    path('inventario/', inventory, name='inventory'),
    path('inventario/<int:id>/', inventory_detail, name='inventory-detail'),
    path('registro/', records, name='records'),
    path('usuario/', user, name='users'),
    path('signin/', login, name='signin'),
    path('signup/', signup, name='signup'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
    path('new-password/', new_password, name='new_password'),
]
