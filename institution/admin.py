from django.contrib import admin
from .models import Institution, Category

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    fields = ("name",)
    show_change_link = True

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "logo_url", "created_at", "updated_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    inlines = (CategoryInline,)
    ordering = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "institution")
    search_fields = ("name", "institution__name")
    list_filter = ("institution",)
    raw_id_fields = ("institution",)
    ordering = ("institution__name", "name")

