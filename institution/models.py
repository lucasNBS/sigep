from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class Institution(models.Model):
    name = models.CharField(max_length=200)
    logo_url = models.ImageField(upload_to="institution/logos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"

    def __str__(self):
        return self.name
    
    def get_permission(self, user):
        try:
            return self.permissions.get(user=user)
        except ObjectDoesNotExist:
            return None
        
    def get_total_users(self):
        return self.permissions.count()
    
    def get_total_itens(self):
        return sum(room.total_itens() for room in self.rooms.all())
    
    def get_total_usable_itens(self):
        return sum(room.total_usable_itens().count() for room in self.rooms.all())
    
    def get_total_lost_itens(self):
        return sum(room.total_lost_itens() for room in self.rooms.all())
    
    def get_total_inventories(self):
        return self.inventories.count()


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