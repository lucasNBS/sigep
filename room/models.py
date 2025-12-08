from django.db import models
from institution.models import Institution

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
