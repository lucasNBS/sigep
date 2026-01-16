from django.db import models

class ConservationState(models.TextChoices):
  NEW = "new", "Ótimo"
  GOOD = "good", "Bom"
  FAIR = "fair", "Usável"
  POOR = "poor", "Ruim"
  UNUSABLE = "unusable", "Inutilizável"
