from django.db import models
from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):
    ADMIN = "admin", "Administrador"
    MANAGER = "manager", "Gerente"
    USER = "user", "Usuário"


class User(AbstractUser):
    photo_url = models.URLField(max_length=500, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.get_full_name() or self.username
