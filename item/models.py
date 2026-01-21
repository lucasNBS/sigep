import uuid
from django.db import models

from . import managers, choices

class Item(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    institution = models.ForeignKey(
        "institution.Institution",
        verbose_name="Instituição",
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField(verbose_name="Nome", max_length=250)
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)
    serial = models.CharField(verbose_name="Serial", max_length=200, default=0)
    invoice_key = models.CharField(verbose_name="Nota Fiscal", max_length=44, default=0)
    notes = models.TextField(verbose_name="Observações", blank=True, null=True)
    category = models.ForeignKey(
        "institution.Category",
        on_delete=models.SET_NULL,
        verbose_name="Categoria",
        null=True,
        blank=True,
        related_name="items",
    )
    room = models.ForeignKey(
        "inventory.Room",
        on_delete=models.SET_NULL,
        verbose_name="Sala",
        null=True,
        blank=True,
        related_name="items",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(
        choices=choices.Status.choices,
        default=choices.Status.FOUND,
    )
    qrcode = models.ImageField(upload_to="qrcodes/", blank=True, null=True)

    objects = managers.SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return f"{self.name}"
    
    def delete(self):
        self.is_deleted = True
        self.save()
    
    def restore(self):
        self.is_deleted = False
        self.save()

    def get_last_record(self):
        self.records.latest("recorded_at")
