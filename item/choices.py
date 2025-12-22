from django.db import models

class Status(models.TextChoices):
  LOST = "lost", "Perdido"
  FOUND = "found", "Localizado"

ACTIVE_STATUS = (
  (None, "---------"),
  (False, "Ativo"),
  (True, "Desativado"),
)