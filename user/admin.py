from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import mark_safe

from .models import User, Permission, Role

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "photo_preview")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "photo_url", "photo_preview")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "password1", "password2", "photo_url"),
        }),
    )

    readonly_fields = ("last_login", "date_joined", "photo_preview")

    def photo_preview(self, obj):
        if not obj or not getattr(obj, "photo_url", None):
            return "-"
        return mark_safe(f'<img src="{obj.photo_url}" style="max-height:50px; max-width:50px; object-fit:cover; border-radius:4px;" />')
    photo_preview.short_description = "Photo"

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("user", "institution", "role_display", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("user__username", "user__first_name", "user__last_name", "institution__name")
    raw_id_fields = ("user", "institution")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def role_display(self, obj):
        for role in Role:
            if role.value == obj.role:
                return role.label
        return obj.role
    role_display.short_description = "Role"

