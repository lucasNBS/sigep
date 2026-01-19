from django.db import models

class ConservationState(models.IntegerChoices):
        NEW = 4,"Novo"
        GOOD = 3,"Bom"
        FAIR = 2,"Utilizável"
        POOR = 1,"Ruim"
        UNUSABLE = 0,"Inutilizável"
