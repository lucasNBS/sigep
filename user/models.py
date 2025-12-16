from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

class Role(Enum):
    ADMIN = ("admin", "Administrador")
    MANAGER = ("manager", "Gerente")
    USER = ("user", "Usuário")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def choices(cls):
        return [(role.value, role.label) for role in cls]


class User(AbstractUser):
    photo_url = models.URLField(max_length=500, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices(),
        default=Role.USER.value,
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.get_full_name() or self.username
