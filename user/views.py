from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, View

from .forms import UserForm, PermissionFormSet

User = get_user_model()


def login(request):
  return render(request, "pages/signin.html", {})

def signup(request):
  return render(request, "pages/signup.html", {})

def forgot_password(request):
  return render(request, "pages/forgot-password.html")

def reset_password(request):
  return render(request, "pages/reset-password.html", {})

def new_password(request):
  return render(request, "pages/new-password.html", {})

class UserListView(ListView):
    model = User
    template_name = "pages/user.html"
    context_object_name = "users"
    paginate_by = 20
    ordering = ("username",)


class UserDetailView(DetailView):
    model = User
    template_name = "pages/user-detail.html"
    context_object_name = "user_obj"


class UserCreateView(View):
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
            return redirect("user:detail", pk=user.pk)

        return render(request, self.template_name, {"form": form, "formset": formset})


class UserUpdateView(View):
    template_name = "pages/user-form.html"

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(instance=user)
        formset = PermissionFormSet(instance=user)
        return render(
            request,
            self.template_name,
            {"form": form, "formset": formset, "user_obj": user},
        )

    @transaction.atomic
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST, request.FILES, instance=user)
        formset = PermissionFormSet(request.POST, instance=user)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect("user:detail", pk=user.pk)

        return render(
            request,
            self.template_name,
            {"form": form, "formset": formset, "user_obj": user},
        )


class UserDeleteView(DeleteView):
    model = User
    template_name = "pages/user-delete.html"
    success_url = reverse_lazy("user:list")
