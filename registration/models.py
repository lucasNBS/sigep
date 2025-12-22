from django.db import models
from django.conf import settings
from item.models import Item

from . import choices

class Record(models.Model):
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
        choices=choices.ConservationState.choices,
        default=choices.ConservationState.GOOD
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return f"Record: {self.item.name} — {self.inventory.title} — {self.conservation_state}"
