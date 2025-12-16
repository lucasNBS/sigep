from django.contrib import admin
from .models import Inventory, InventoryItem, Room

class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 1
    fields = ("item", "quantity", "notes")
    raw_id_fields = ("item",)
    show_change_link = True

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "responsible", "start_date", "end_date", "created_at")
    search_fields = ("title", "institution__name", "responsible__username", "responsible__email")
    list_filter = ("institution",)
    raw_id_fields = ("institution", "responsible")
    readonly_fields = ("created_at", "updated_at")
    inlines = (InventoryItemInline,)
    ordering = ("-created_at",)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("inventory", "item", "quantity")
    search_fields = ("inventory__title", "item__name")
    raw_id_fields = ("inventory", "item")
    ordering = ("inventory__title", "item__name")

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "institution")
    search_fields = ("name", "institution__name")
    list_filter = ("institution",)
    raw_id_fields = ("institution",)
    ordering = ("institution__name", "name")
