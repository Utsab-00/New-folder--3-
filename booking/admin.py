from django.contrib import admin
from .models import Booking, Event
from django.utils.html import format_html

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'seat', 'token', 'qr_preview')
    list_filter = ('event', 'seat')
    search_fields = ('user__username', 'token')

    def qr_preview(self, obj):
        if obj.qr_path and hasattr(obj.qr_path, 'url'):
            return format_html('<img src="{}" width="80"/>', obj.qr_path.url)
        return "No QR"
    qr_preview.short_description = "QR Code"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'date', 'location')