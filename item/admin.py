from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "institution", "category", "room", "serial", "created_at")
    list_filter = ("institution", "category", "room")
    search_fields = ("name", "serial", "invoice_key", "notes")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    def get_queryset(self, request):
        return Item.all_objects.all()
