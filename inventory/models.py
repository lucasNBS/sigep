from django.db import models
from django.db.models import OuterRef, Subquery
from django.conf import settings
from django.core.exceptions import ValidationError

from institution.models import Institution
from item.choices import Status as ItemStatus
from item.models import Item
from registration.choices import ConservationState
from registration.models import Record

from .choices import Status

        

class Room(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="rooms"
    )
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def clean(self):
        if Room.objects.filter(name=self.name, institution=self.institution).exclude(id=self.id).exists():
            raise ValidationError("Sala com este nome já existe")

    def __str__(self):
        return f"{self.name}"
    
    def total_itens(self):
        return self.items.count()
    
    def total_lost_itens(self):
        return self.items.filter(status=ItemStatus.LOST).count()
    
    def get_usable_itens(self):
        return self.items.annotate(
            state=Subquery(
                Record.objects.filter(item=OuterRef("pk"))
                .order_by("-recorded_at")
                .values("conservation_state")[:1]
            )
        ).filter(state__gt=ConservationState.FAIR)


class Inventory(models.Model):
    title = models.CharField(max_length=250)
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="inventories"
    )
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="inventories",
    )
    leader_consultor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="lead",
    )
    consultors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="consultories",
        blank=False,
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.OPEN,
    )

    rooms = models.ManyToManyField(
        Room,
        related_name="inventories",
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"
    
    def get_total_itens(self):
        return sum(room.total_itens() for room in self.rooms.all())
    
    def get_total_itens_registered(self):
        return Record.objects.filter(inventory=self).count()

    def get_total_itens_pending(self):
        return self.get_total_itens() - self.get_total_itens_registered()
    
    def get_progress(self):
        total = self.get_total_itens()
        if total == 0 :
            return "0%"
        else :
            return f"{self.get_total_itens_registered()/total:.0%}"
