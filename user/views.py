from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from core.views import BaseContextView, AccessMixin
from institution.models import Institution

from .forms import SignupForm, UserSelfUpdateForm, UserFilterForm
from .models import Permission, Role, PasswordResetCode, UserInvitation

from .tasks import send_email_with_otp, send_invite_email

User = get_user_model()

MAX_ATTEMPTS = 5


class SigninView(View):
    template_name = "pages/signin.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")

        next_url = request.GET.get("next", "")
        return render(request, self.template_name, {"next": next_url})

    def post(self, request):
        email = request.POST.get("username", "").strip().lower()
        password = request.POST.get("password", "")
        next_url = request.POST.get("next") or request.GET.get("next") or ""

        try:
            user_obj = User.objects.get(email__iexact=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if not user:
            messages.error(request, "E-mail ou senha inválidos.")
            return render(request, self.template_name, {"next": next_url})

        auth_login(request, user)

        request.session.pop("institution_id", None)
        request.session.pop("role", None)
        request.session.pop("next_after_institution", None)

        perms = (
            Permission.objects.filter(user=user, revoked_at__isnull=True)
            .select_related("institution")
            .order_by("institution__name")
        )

        if not perms.exists():
            messages.error(request, "Seu usuário não possui instituições vinculadas.")
            return redirect("dashboard")

        if perms.count() == 1:
            perm = perms.first()
            request.session["institution_id"] = perm.institution_id
            request.session["role"] = perm.role
            return redirect(next_url or "dashboard")

        if next_url:
            request.session["next_after_institution"] = next_url
        return redirect("dashboard")


class LogoutView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"

    def post(self, request):
        auth_logout(request)
        request.session.flush()
        return redirect("signin")

    def get(self, request):
        return self.post(request)


class SignupView(View):
    template_name = "pages/signup.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        form = SignupForm()
        return render(request, self.template_name, {"form": form})

    @transaction.atomic
    def post(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")

        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.email = user.email.lower()
            user.save()

            code = request.GET.get('code')

            if code:
                hash_code = UserInvitation.hash_code(code)
                user_invitation = UserInvitation.objects.filter(
                    email=user.email, code_hash=hash_code
                )

                if user_invitation.exists():
                    for invitation in user_invitation:
                        Permission.objects.create(
                            user=user, institution=invitation.institution, role=invitation.role
                        )

            auth_login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("dashboard")

        return render(request, self.template_name, {"form": form})


class ForgotPasswordView(View):
    template_name = "pages/forgot-password.html"
    code_ttl_minutes = 10

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = (request.POST.get("email") or "").strip().lower()
        
        messages.success(
            request,
            "Se este e-mail estiver cadastrado, enviaremos um código de verificação.",
        )
        
        user = User.objects.filter(email__iexact=email).first()
        if user:
            PasswordResetCode.objects.filter(
                user=user,
                used_at__isnull=True,
            ).update(used_at=timezone.now())

            raw_code = PasswordResetCode.generate_code(5)
            PasswordResetCode.objects.create(
                user=user,
                code_hash=PasswordResetCode.hash_code(raw_code),
                expires_at=timezone.now() + timedelta(minutes=self.code_ttl_minutes),
            )

            try:
                send_email_with_otp.delay(email, raw_code)
                print("[DEV] E-mail enviado com sucesso para", email)
                messages.success(request, 'E-mail enviado com sucesso!')
            except Exception as e:
                print("[DEV] Erro ao enviar e-mail para", email, ":", str(e))
                messages.error(request, 'Erro ao enviar o formulário')

        request.session["pwreset_email"] = email
        return redirect("reset-password")


class ResetPasswordView(View):
    template_name = "pages/reset-password.html"

    def get(self, request):
        email = request.session.get("pwreset_email", "") or request.GET.get("email", "")
        next_url = request.session.get("pwreset_next", "") or request.GET.get("next", "")
        return render(request, self.template_name, {"email": email, "next": next_url})

    def post(self, request):
        print("[DEV] reset-password POST:", dict(request.POST))
        email = (request.POST.get("email") or "").strip().lower()
        code = (request.POST.get("code") or "").strip()
        print("[DEV] email:", repr(email), "code:", repr(code), "len(code):", len(code))
        next_url = (request.POST.get("next") or "").strip()

        if next_url:
            request.session["pwreset_next"] = next_url

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            messages.error(request, "Código inválido ou expirado.")
            return redirect("reset-password")

        prc = (
            PasswordResetCode.objects
            .filter(user=user, used_at__isnull=True)
            .order_by("-created_at")
            .first()
        )

        if not prc or prc.is_expired():
            messages.error(request, "Código inválido ou expirado.")
            return redirect("reset-password")

        if prc.attempts >= MAX_ATTEMPTS:
            messages.error(request, "Você excedeu o número de tentativas. Solicite um novo código.")
            return redirect("forgot-password")

        prc.attempts += 1
        prc.save(update_fields=["attempts"])

        if prc.code_hash != PasswordResetCode.hash_code(code):
            messages.error(request, "Código inválido ou expirado.")
            return redirect("reset-password")

        request.session["pwreset_email"] = email
        request.session["pwreset_code"] = code
        request.session["pwreset_ok"] = True
        request.session["pwreset_verified_at"] = timezone.now().isoformat()

        return redirect("new-password")


class NewPasswordView(View):
    template_name = "pages/new-password.html"

    def get(self, request):
        email = (request.session.get("pwreset_email") or "").strip().lower()
        code = (request.session.get("pwreset_code") or "").strip()
        ok = request.session.get("pwreset_ok", False)

        if not ok or not email or not code:
            messages.error(request, "Sessão de redefinição inválida. Solicite um novo código.")
            return redirect("forgot-password")

        next_url = request.session.get("pwreset_next", "") or request.GET.get("next", "")
        return render(request, self.template_name, {"email": email, "next": next_url})

    def post(self, request):
        email = (request.session.get("pwreset_email") or "").strip().lower()
        code = (request.session.get("pwreset_code") or "").strip()
        ok = request.session.get("pwreset_ok", False)

        if not ok or not email or not code:
            messages.error(request, "Sessão de redefinição inválida. Solicite um novo código.")
            return redirect("forgot-password")

        next_url = (request.POST.get("next") or "").strip()
        if next_url:
            request.session["pwreset_next"] = next_url

        p1 = request.POST.get("new_password1") or ""
        p2 = request.POST.get("new_password2") or ""

        if p1 != p2:
            messages.error(request, "As senhas não conferem.")
            return redirect("new-password")

        if len(p1) < 8:
            messages.error(request, "A senha deve ter pelo menos 8 caracteres.")
            return redirect("new-password")

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            messages.error(request, "Não foi possível redefinir a senha.")
            return redirect("forgot-password")

        prc = (
            PasswordResetCode.objects
            .filter(user=user, used_at__isnull=True)
            .order_by("-created_at")
            .first()
        )

        if not prc or prc.is_expired():
            messages.error(request, "Código inválido ou expirado. Solicite um novo código.")
            return redirect("forgot-password")

        if prc.code_hash != PasswordResetCode.hash_code(code):
            messages.error(request, "Código inválido ou expirado. Solicite um novo código.")
            return redirect("reset-password")

        user.set_password(p1)
        user.save(update_fields=["password"])

        prc.used_at = timezone.now()
        prc.save(update_fields=["used_at"])

        for k in ["pwreset_email", "pwreset_code", "pwreset_ok", "pwreset_verified_at"]:
            request.session.pop(k, None)

        messages.success(request, "Senha redefinida com sucesso. Você já pode entrar com a nova senha.")

        next_to = request.session.pop("pwreset_next", "") or ""
        if next_to:
            return redirect(next_to)

        return redirect("signin")


class DashboardView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"
    template_name = "pages/dashboard.html"

    def get(self, request):
        permission_list = (
            Permission.objects
            .filter(user=request.user, revoked_at__isnull=True)
            .select_related("institution")
            .order_by("institution__name")
        )


        role_map = dict(Role.choices())

        institutions = [
            {
                "id": perms.institution.id,
                "name": perms.institution.name,
                "role_value": perms.role,
                "role_label": role_map.get(perms.role, perms.role),
            }
            for perms in permission_list
        ]

        return render(request, self.template_name, {"institutions": institutions})


class SelectInstitutionView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"

    def get(self, request, institution_id):
        perm = get_object_or_404(
            Permission,
            user=request.user,
            institution_id=institution_id,
            revoked_at__isnull=True,
        )


        request.session["institution_id"] = perm.institution_id
        request.session["role"] = perm.role
        request.session["institution_name"] = perm.institution.name

        next_url = request.session.pop("next_after_institution", None)
        return redirect(next_url or "institution")

    def post(self, request, institution_id):
        perm = get_object_or_404(
            Permission,
            user=request.user,
            institution_id=institution_id, 
            revoked_at__isnull=True,
        )

        request.session["institution_id"] = perm.institution_id
        request.session["role"] = perm.role
        request.session["institution_name"] = perm.institution.name

        next_url = request.session.pop("next_after_institution", None)
        return redirect(next_url or "institution")


class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"
    template_name = "pages/profile.html"

    def get(self, request):
        user = request.user
        context = {
            "user_obj": user,
            "user_photo": user.photo_url,
            "form": UserSelfUpdateForm(instance=user),
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        user = request.user
        form = UserSelfUpdateForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("profile")

        context = {
            "user_obj": user,
            "user_photo": user.photo_url,
            "form": form,
        }
        return render(request, self.template_name, context)

class UserListView(AccessMixin, BaseContextView, ListView):
    login_url = "signin"
    redirect_field_name = "next"

    model = Permission
    template_name = "pages/user.html"
    context_object_name = "permissions"

    def dispatch(self, request, *args, **kwargs):
        self.check_has_admin_access()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        role = request.POST.get('role')

        user = User.objects.filter(email=email)
        institution = Institution.objects.get(id=self.kwargs.get('institution_id'))

        if user.exists():
            Permission.objects.create(
                user=user.first(), institution=institution, role=Role.get(role).value
            )
            send_invite_email.delay(
                email,
                f"Você foi convidado à se jutar a instituição {institution} no sistema SIGEP como um {Role.get(role).label}. Acesse o sistema através do link https://w5txwvqw-80.brs.devtunnels.ms/"
            )
        else:
            raw_code = UserInvitation.generate_code(5)
            UserInvitation.objects.create(
                role=Role.get(role).value,
                email=email,
                institution=institution,
                code_hash=UserInvitation.hash_code(raw_code)
            )
            send_invite_email.delay(
                email,
                f"Você foi convidado à se jutar a instituição {institution} no sistema SIGEP como um {Role.get(role).label}. Acesse o sistema através do link https://w5txwvqw-80.brs.devtunnels.ms/conta/criar/?code={raw_code}"
            )
        url = reverse(
            'permission-list', kwargs={'institution_id': self.kwargs.get('institution_id')}
        )
        return HttpResponseRedirect(url)

    def get_paginate_by(self, queryset):
        page_size = self.request.GET.get("size")
        if page_size:
            return page_size
        return 10

    def get_queryset(self):
        institution_id = self.kwargs.get("institution_id")

        if not institution_id:
            return Permission.objects.none()

        permissions_qs = (
            Permission.objects
            .select_related("user", "institution")
            .filter(institution__id=institution_id, revoked_at__isnull=True)
            .exclude(user=self.request.user)
        )

        filter_form = UserFilterForm(self.request.GET or None)
        if filter_form.is_valid():
            name = (filter_form.cleaned_data.get("name") or "").strip()
            email = (filter_form.cleaned_data.get("email") or "").strip()
            role = filter_form.cleaned_data.get("role") or ""

            if name:
                terms = [term for term in name.split() if term.strip()]
                for term in terms:
                    permissions_qs = permissions_qs.filter(
                    Q(user__first_name__icontains=term) |
                    Q(user__last_name__icontains=term) |
                    Q(user__username__icontains=term)
                )

            if email:
                permissions_qs = permissions_qs.filter(
                    Q(user__email__icontains=email) |
                    Q(user__username__icontains=email)
                )

            if role and role != "admin":
                permissions_qs = permissions_qs.filter(role=role)

        return permissions_qs.order_by("user__first_name", "user__username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["size"] = self.request.GET.get("size") if self.request.GET.get('size') else 10
        context["filter_form"] = UserFilterForm(self.request.GET or None)
        context["querystring"] = self.request.GET.urlencode()
        return context


class UserDetailView(AccessMixin, BaseContextView, DetailView):
    login_url = "signin"
    redirect_field_name = "next"

    model = Permission
    template_name = "pages/user-detail.html"
    context_object_name = "user_obj"
    pk_url_kwarg = "permission_id"

    def dispatch(self, request, *args, **kwargs):
        self.check_has_admin_access()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        institution_id = self.kwargs.get("institution_id")
        if institution_id:
            permission = (
                Permission.objects
                .select_related("institution")
                .filter(
                    user=self.object.user, institution_id=institution_id, revoked_at__isnull=True
                )
                .first()
            )
        else:
            permission = None

        context["permission"] = permission
        context["remove_action_url"] = (
            reverse("permission-delete", kwargs={
                "institution_id": institution_id,"permission_id": permission.pk
            })
        )

        return context


class PermissionUpdateView(AccessMixin, View):

    def dispatch(self, request, *args, **kwargs):
        self.check_has_admin_access()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, institution_id, permission_id):
        perm = get_object_or_404(
            Permission,
            pk=permission_id,
            institution_id=institution_id,
            revoked_at__isnull=True,
        )

        perm.role = request.POST.get("role")
        perm.save(update_fields=["role"])

        return redirect("permission-list")


class PermissionRevokeView(AccessMixin, View):

    def dispatch(self, request, *args, **kwargs):
        self.check_has_admin_access()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, institution_id, permission_id):
        perm = get_object_or_404(
            Permission,
            pk=permission_id,
            institution_id=institution_id,
            revoked_at__isnull=True,
        )
        perm.revoke()
        return redirect('permission-list')
