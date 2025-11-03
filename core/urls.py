from django.contrib import admin
from django.urls import path

from core.views import home, login, signup, forgot_password, reset_password, new_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signin/', login, name='signin'),
    path('signup/', signup, name='signup'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
    path('new-password/', new_password, name='new_password'),
]
