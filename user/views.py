from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, View

from .forms import UserForm, PermissionFormSet
from .models import Permission

User = get_user_model()


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            next_url = request.POST.get("next") or request.GET.get("next")
            return redirect(next_url or reverse("users"))

        messages.error(request, "Usuário ou senha inválidos.")

    next_url = request.GET.get("next", "")
    return render(request, "pages/signin.html", {"next": next_url})


def signup(request):
    return render(request, "pages/signup.html", {})


def forgot_password(request):
    return render(request, "pages/forgot-password.html", {})


def reset_password(request):
    return render(request, "pages/reset-password.html", {})


def new_password(request):
    return render(request, "pages/new-password.html", {})


class UserListView(LoginRequiredMixin, ListView):
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

        formset = PermissionFormSet(request.POST) if request.method == "POST" else PermissionFormSet()
        return render(request, self.template_name, {"form": form, "formset": formset})


class UserUpdateView(LoginRequiredMixin, View):
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
    model = User
    template_name = "pages/user-delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("users")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Usuário removido com sucesso!")
        return super().delete(request, *args, **kwargs)
