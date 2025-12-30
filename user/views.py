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
            return redirect(reverse("dashboard"))

        next_url = request.GET.get("next", "")
        return render(request, self.template_name, {"next": next_url})

    def post(self, request):
        email = request.POST.get("username", "").strip().lower()
        password = request.POST.get("password", "")

        try:
            user_obj = User.objects.get(email__iexact=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)

            perm = (
                Permission.objects
                .filter(user=user)
                .order_by("created_at")
                .first()
            )

            if perm:
                request.session["role"] = perm.role
            else:
                request.session.pop("role", None)

            next_url = request.POST.get("next") or request.GET.get("next")
            return redirect(next_url or reverse("dashboard"))

        messages.error(request, "E-mail ou senha inválidos.")
        next_url = request.POST.get("next", "")
        return render(request, self.template_name, {"next": next_url})


class LogoutView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"

    def post(self, request):
        auth_logout(request)
        request.session.flush()
        return redirect(reverse("signin"))

    def get(self, request):
        return self.post(request)


class SignupView(View):
    template_name = "pages/signup.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("dashboard"))
        form = SignupForm()
        return render(request, self.template_name, {"form": form})

    @transaction.atomic
    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("dashboard"))

        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.email = user.email.lower()
            user.save()

            auth_login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect(reverse("dashboard"))

        return render(request, self.template_name, {"form": form})



def forgot_password(request):
  return render(request, "pages/forgot-password.html")

def reset_password(request):
  return render(request, "pages/reset-password.html", {})

def new_password(request):
  return render(request, "pages/new-password.html", {})



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

        if form.is_valid():
            user = form.save()

            formset = PermissionFormSet(request.POST, instance=user)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Usuário cadastrado com sucesso!")
                return redirect("users-detail", id=user.pk)

        formset = PermissionFormSet(request.POST)
        return render(request, self.template_name, {"form": form, "formset": formset})

class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"
    template_name = "pages/profile.html"

    def _get_institutions(self, user):
        perms = (
            Permission.objects
            .select_related("institution")
            .filter(user=user)
            .order_by("institution__name")
        )

        return [
            {
                "company_name": p.institution.name,
                "role": dict(Role.choices()).get(p.role, p.role),
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
        form = UserSelfUpdateForm(request.POST, instance=user)

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
    login_url = "signin"
    redirect_field_name = "next"
    template_name = "pages/profile.html"

    def get(self, request):
        user = request.user
        
        perms = (
            Permission.objects
            .select_related("institution")
            .filter(user=user)
            .order_by("institution__name")
        )

        institutions = [
            {
                "company_name": p.institution.name,
                "role": dict(Role.choices()).get(p.role, p.role),
                "items_total": None,
                "users_total": None,
            }
            for p in perms
        ]

        context = {
            "user_obj": user,
            "user_photo": user.photo_url,
            "institutions": institutions,
            "form": UserSelfUpdateForm(instance=user),
        }
        return render(request, self.template_name, context)
    redirect_field_name = "next"
    template_name = "pages/profile.html"

    @transaction.atomic
    def get(self, request):
        user = request.user
        form = UserSelfUpdateForm(instance=user) 
        return render(request, self.template_name, {"form": form, "user_obj": user})

    @transaction.atomic
    def post(self, request):
        user = request.user
        form = UserSelfUpdateForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("profile")  # ajuste para o nome real da sua rota

        return render(request, self.template_name, {"form": form, "user_obj": user})

class UserUpdateView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "next"
    template_name = "pages/user-form.html"

    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        form = UserForm(instance=user)
        formset = PermissionFormSet(instance=user)

        return render(request, self.template_name, {
            "form": form,
            "formset": formset,
            "user_obj": user
        })

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

        return render(request, self.template_name, {
            "form": form,
            "formset": formset,
            "user_obj": user
        })
    login_url = "signin"
    redirect_field_name = "next"

    template_name = "pages/profile.html"

    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        form = UserForm(instance=user)
        formset = PermissionFormSet(instance=user)
        return render(request, self.template_name, {"form": form, "formset": formset, "user_obj": user})

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

        return render(request, self.template_name, {"form": form, "formset": formset, "user_obj": user})


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
