from django.contrib import admin
from .models import Booking, Event

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'seat', 'token', 'qr_path')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title',)  # ✅ This must match your model field