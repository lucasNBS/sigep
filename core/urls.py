from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import profile
from institution.views import ListInstitutionsView
from user.views import SigninView, LogoutView, SignupView, ForgotPasswordView, ResetPasswordView, NewPasswordView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("conta/login/", SigninView.as_view(), name="signin"),
    path("conta/logout/", LogoutView.as_view(), name="logout"),
    path("conta/criar/", SignupView.as_view(), name="signup"),
    path("conta/esqueceu-senha/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("conta/redefinir-senha/", ResetPasswordView.as_view(), name="reset-password"),
    path("conta/nova-senha/", NewPasswordView.as_view(), name="new-password"),

    path('instituicao/', include('institution.urls')),
    path('', ListInstitutionsView.as_view(), name='dashboard'),
    path('', include('user.urls')),
    path('perfil/', profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
