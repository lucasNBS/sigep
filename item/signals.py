import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Item


@receiver(post_save, sender=Item)
def create_qrcode(sender, instance, created, **kwargs):
  if not created or instance.qrcode:
    return

  url = f"https://w5txwvqw-80.brs.devtunnels.ms/instituicao/{instance.institution.id}/patrimonio/{instance.id}/registrar/"

  qr = qrcode.make(url)

  buffer = BytesIO()
  qr.save(buffer, format="PNG")

  instance.qrcode.save(f"{instance.id}.png", ContentFile(buffer.getvalue()), save=True)
