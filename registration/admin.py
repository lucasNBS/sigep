from django.contrib import admin
from .models import Record

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("item", "inventory", "user", "conservation_state", "recorded_at")
    list_filter = ("conservation_state", "inventory", "user")
    search_fields = ("item__name", "inventory__title", "user__username", "notes")
    readonly_fields = ("recorded_at",)
    ordering = ("-recorded_at",)

