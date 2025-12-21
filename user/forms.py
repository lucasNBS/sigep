from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

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
