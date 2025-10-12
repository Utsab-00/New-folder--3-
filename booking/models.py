from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    title = models.CharField(max_length=100, default='unknown event')

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seat = models.CharField(max_length=10)
    token = models.CharField(max_length=255)
    qr_path = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    timestamp = models.DateTimeField(default=now)
    downloaded = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    last_downloaded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.seat}"

class DownloadLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} downloaded {self.booking.token} at {self.timestamp}"