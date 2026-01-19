from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from enum import Enum
from django.utils import timezone
import hashlib
import secrets


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
    photo_url = models.ImageField(upload_to="user/photos/", blank=True, null=True)

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
    
    revoked_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "institution")
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        
    def revoke(self):
        if self.revoked_at is not None:
            return
        self.revoked_at = timezone.now()
        self.save(update_fields=["revoked_at"])

    def reactivate(self):
        if self.revoked_at is None:
            return
        self.revoked_at = None
        self.save(update_fields=["revoked_at"]) 

    def __str__(self):
        return f"{self.user} — {self.institution} — {self.role}"
    
class PasswordResetCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_codes",
    )

    code_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def is_used(self):
        return self.used_at is not None

    @staticmethod
    def generate_code(length=6):
        return "".join(str(secrets.randbelow(10)) for _ in range(length))

    @staticmethod
    def hash_code(raw_code: str) -> str:
        return hashlib.sha256(raw_code.encode()).hexdigest()