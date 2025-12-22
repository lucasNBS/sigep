from django.db import models
from django.core.exceptions import ValidationError


class Institution(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"

    def __str__(self):
        return self.name
    
class Category(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def clean(self):
        if Category.objects.filter(name=self.name, institution=self.institution).exclude(id=self.id).exists():
            raise ValidationError("Sala com este nome já existe")

    def __str__(self):
        return f"{self.name}"