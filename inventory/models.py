from django.db import models
from django.conf import settings
from institution.models import Institution
from item.models import Item
from enum import Enum

class Status(Enum):
    OPEN = ("Aberto","aberto")
    CLOSED = ("Encerrado", "encerrado")
    IMPORTED = ("Importação Finalizada", "importado")
    CONCILIATED= ("Conciliado", "conciliado")


    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def choices(cls):
        return [(status.value, status.label) for status in cls]
        

class Room(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="rooms"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        unique_together = ("institution", "name")

    def __str__(self):
        return f"{self.name} — {self.institution.name}"


class Inventory(models.Model):
    title = models.CharField(max_length=250)
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="inventories"
    )
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inventories",
    )
    leader_consultor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lead",
    )
    consultors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="consultories",
        blank=True,
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    items = models.ManyToManyField(
        Item,
        related_name="inventories",
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices(),
        default=Status.OPEN.value,
    )

    rooms = models.ManyToManyField(
        Room,
        related_name="inventories",
        blank=True,
    )


