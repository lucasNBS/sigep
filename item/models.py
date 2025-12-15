from django.db import models
from django.conf import settings


class Item(models.Model):
    institution = models.ForeignKey(
        "institution.Institution", on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    serial = models.CharField(max_length=200, blank=True, null=True)
    invoice_key = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        "institution.Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="items"
    )
    room = models.ForeignKey(
        "inventory.Room", on_delete=models.SET_NULL, null=True, blank=True, related_name="items"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        unique_together = (("institution", "name", "serial"),)

    def __str__(self):
        return f"{self.name} ({self.institution.name})"


class Record(models.Model):
    class ConservationState(models.TextChoices):
        NEW = "new", "New"
        GOOD = "good", "Good"
        FAIR = "fair", "Fair"
        POOR = "poor", "Poor"
        UNUSABLE = "unusable", "Unusable"

    inventory = models.ForeignKey(
        "inventory.Inventory", on_delete=models.CASCADE, related_name="records"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="records"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="records"
    )
    notes = models.TextField(blank=True, null=True)
    conservation_state = models.CharField(
        max_length=20,
        choices=ConservationState.choices,
        default=ConservationState.GOOD
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return f"Record: {self.item.name} — {self.inventory.title} — {self.conservation_state}"
