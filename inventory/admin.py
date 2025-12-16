from django.contrib import admin
from .models import Inventory, Room

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "responsible", "start_date", "end_date", "created_at")
    search_fields = ("title", "institution__name", "responsible__username", "responsible__email")
    list_filter = ("institution",)
    raw_id_fields = ("institution", "responsible")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "institution")
    search_fields = ("name", "institution__name")
    list_filter = ("institution",)
    raw_id_fields = ("institution",)
    ordering = ("institution__name", "name")
