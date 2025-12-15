from django.db import models
from django.conf import settings
from institution.models import Institution
from item.models import Item

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
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    items = models.ManyToManyField(
        Item,
        through="InventoryItem",
        related_name="inventories",
        blank=True,
    )

class InventoryItem(models.Model):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="inventory_items"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="inventory_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Inventory - Item"
        verbose_name_plural = "Inventories - Items"
        constraints = [
            models.UniqueConstraint(
                fields=["inventory", "item"],
                name="unique_inventory_item"
            )
        ]

    def __str__(self):
        return f"{self.inventory.title} ↔ {self.item.name}"


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
