from django.urls import path
from .views import institution

urlpatterns = [
    path('', institution, name='institution'),
]
