from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from enum import Enum

class Role(Enum):
    ADMIN = ("admin", "Administrador")
    MANAGER = ("manager", "Gerente de Patrimônio")
    USER = ("user", "Consultor de Patrimônio")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def choices(cls):
        return [(role.value, role.label) for role in cls]


class User(AbstractUser):
    photo_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.get_full_name() or self.username


class Permission(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="permissions",
        on_delete=models.CASCADE,
    )
    institution = models.ForeignKey(
        "institution.Institution",
        related_name="permissions",
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices(),
        default=Role.USER.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "institution")
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self):
        return f"{self.user} — {self.institution} — {self.role}"