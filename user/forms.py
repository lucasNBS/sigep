from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify

from .models import Permission

User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "photo_url",
            "is_active",
        )

PermissionFormSet = inlineformset_factory(
    parent_model=User,
    model=Permission,
    fields=("institution", "role"),
    extra=1,
    can_delete=True,
)

class SignupForm(UserCreationForm):
    full_name = forms.CharField(
        label="Nome",
        max_length=150,
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe um usuário com esse e-mail.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        full_name = self.cleaned_data["full_name"].strip()
        parts = full_name.split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""

        base_username = slugify(full_name).replace("-", "") or "user"
        username = base_username
        i = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{i}"
            i += 1

        user.username = username
        user.email = self.cleaned_data["email"].lower()
        user.is_active = True

        if commit:
            user.save()
        return user
    
class UserSelfUpdateForm(forms.ModelForm):
    full_name = forms.CharField(
        label="Nome",
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "Nome completo"
        })
    )

    class Meta:
        model = User
        fields = ("full_name", "photo_url",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance:
            self.fields["full_name"].initial = self.instance.get_full_name()

    def save(self, commit=True):
        user = super().save(commit=False)

        full_name = (self.cleaned_data.get("full_name") or "").strip()
        parts = full_name.split()

        if parts:
            user.first_name = parts[0]
            user.last_name = " ".join(parts[1:])
        else:
            user.first_name = ""
            user.last_name = ""

        if commit:
            user.save()

        return user