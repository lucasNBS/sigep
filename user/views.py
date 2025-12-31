from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

from .forms import UserForm, PermissionFormSet, SignupForm, UserSelfUpdateForm
from .models import Permission, Role

User = get_user_model()

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
            Permission.objects
            .filter(user=user)
            .select_related("institution")
            .order_by("institution__name")
        )

        if not perms.exists():
            auth_logout(request)
            messages.error(request, "Seu usuário não possui instituições vinculadas.")
            return redirect("signin")

        if perms.count() == 1:
            perm = perms.first()
            request.session["institution_id"] = perm.institution_id
            request.session["role"] = perm.role
            return redirect(next_url or "institution")

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

            auth_login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("dashboard")

        return render(request, self.template_name, {"form": form})


def forgot_password(request):
    return render(request, "pages/forgot-password.html")


def reset_password(request):
    return render(request, "pages/reset-password.html", {})


def new_password(request):
    return render(request, "pages/new-password.html", {})




class DashboardView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"
    template_name = "pages/dashboard.html"

    def get(self, request):
        perms = (
            Permission.objects
            .filter(user=request.user)
            .select_related("institution")
            .order_by("institution__name")
        )

        role_map = dict(Role.choices())

        institutions = [
            {
                "id": p.institution.id,
                "name": p.institution.name,
                "role_value": p.role,
                "role_label": role_map.get(p.role, p.role),
            }
            for p in perms
        ]

        return render(request, self.template_name, {"institutions": institutions})


class SelectInstitutionView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"

    def get(self, request, institution_id):
        perm = get_object_or_404(
            Permission,
            user=request.user,
            institution_id=institution_id
        )

        request.session["institution_id"] = perm.institution_id
        request.session["role"] = perm.role

        next_url = request.session.pop("next_after_institution", None)
        return redirect(next_url or "institution")
    redirect_field_name = "next"

    def post(self, request, institution_id):
        perm = get_object_or_404(
            Permission,
            user=request.user,
            institution_id=institution_id
        )

        request.session["institution_id"] = perm.institution_id
        request.session["role"] = perm.role

        next_url = request.session.pop("next_after_institution", None)
        return redirect(next_url or "institution")



class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"
    template_name = "pages/profile.html"

    def _get_institutions(self, user):
        perms = (
            Permission.objects
            .filter(user=user)
            .select_related("institution")
            .order_by("institution__name")
        )
        role_map = dict(Role.choices())

        return [
            {
                "company_name": p.institution.name,
                "role": role_map.get(p.role, p.role),
                "items_total": None,
                "users_total": None,
            }
            for p in perms
        ]

    def get(self, request):
        user = request.user
        context = {
            "user_obj": user,
            "user_photo": user.photo_url,
            "institutions": self._get_institutions(user),
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
            "institutions": self._get_institutions(user),
            "form": form,
        }
        return render(request, self.template_name, context)



class UserListView(LoginRequiredMixin, ListView):
    login_url = "signin"
    redirect_field_name = "next"

    model = Permission
    template_name = "pages/user.html"
    context_object_name = "permissions"
    paginate_by = 20

    def get_queryset(self):
        return (
            Permission.objects
            .select_related("user", "institution")
            .order_by("user__first_name", "user__username")
        )


class UserDetailView(LoginRequiredMixin, DetailView):
    login_url = "signin"
    redirect_field_name = "next"

    model = User
    template_name = "pages/user-detail.html"
    context_object_name = "user_obj"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permission"] = (
            Permission.objects
            .select_related("institution")
            .filter(user=self.object)
            .first()
        )
        return context


class UserCreateView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"

    template_name = "pages/user-form.html"

    def get(self, request):
        form = UserForm()
        formset = PermissionFormSet()
        return render(request, self.template_name, {"form": form, "formset": formset})

    @transaction.atomic
    def post(self, request):
        form = UserForm(request.POST, request.FILES)
        formset = PermissionFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            user = form.save()
            formset.instance = user
            formset.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect("users-detail", id=user.pk)

        return render(request, self.template_name, {"form": form, "formset": formset})


class UserUpdateView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"
    template_name = "pages/user-form.html"

    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        form = UserForm(instance=user)
        formset = PermissionFormSet(instance=user)
        return render(
            request,
            self.template_name,
            {"form": form, "formset": formset, "user_obj": user},
        )

    @transaction.atomic
    def post(self, request, id):
        user = get_object_or_404(User, pk=id)
        form = UserForm(request.POST, request.FILES, instance=user)
        formset = PermissionFormSet(request.POST, instance=user)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect("users-detail", id=user.pk)

        return render(
            request,
            self.template_name,
            {"form": form, "formset": formset, "user_obj": user},
        )


class UserDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "signin"
    redirect_field_name = "next"

    model = User
    template_name = "pages/user-delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("users")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Usuário removido com sucesso!")
        return super().delete(request, *args, **kwargs)
