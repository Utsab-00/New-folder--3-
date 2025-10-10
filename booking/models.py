from django.db import models
from django.utils.timezone import now

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

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

    def __str__(self):
        return f"{self.user} - {self.event} - {self.seat}"
