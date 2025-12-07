from django.urls import path
from .views import institution

urlpatterns = [
    path('instituicao/', institution, name='institution'),
]
