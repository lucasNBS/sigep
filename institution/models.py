from django.db import models

class Institution(models.Model):
    name = models.CharField(max_length=200)
    logo_url = models.ImageField(upload_to="institution/logos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"
        unique_together = ("name",)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        unique_together = ("institution", "name")

    def __str__(self):
        return f"{self.name} — {self.institution.name}"