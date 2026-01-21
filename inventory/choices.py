from django.db import models

class Status(models.TextChoices):
    OPEN = "Aberto","aberto"
    CLOSED = "Encerrado", "encerrado"
    IMPORTED = "Importação Finalizada", "importado"
    CONCILIATED= "Conciliado", "conciliado"


