from django.contrib import admin
from .models import Booking, Event, DownloadLog
from django.utils.html import format_html

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'seat', 'download_count', 'last_downloaded', 'qr_preview')
    list_filter = ('event', 'download_count')
    search_fields = ('user__username', 'token', 'seat')
    readonly_fields = ('token', 'timestamp', 'download_count', 'last_downloaded')

    def qr_preview(self, obj):
        if obj.qr_path:
            return format_html('<img src="{}" width="80"/>', obj.qr_path.url)
        return "No QR"
    qr_preview.short_description = "QR Code"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    list_filter = ('date',)
    search_fields = ('title', 'location')

@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ('booking', 'ip_address', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('booking__user__username', 'ip_address')
    readonly_fields = ('booking', 'ip_address', 'timestamp')