from django.db import models

class ConservationState(models.TextChoices):
        NEW = "Novo", "New"
        GOOD = "Bom", "Good"
        FAIR = "Utilizável", "Fair"
        POOR = "Ruim", "Poor"
        UNUSABLE = "Inutilizável", "Unusable"
