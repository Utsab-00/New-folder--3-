from django.db import models
from django.utils.timezone import now

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seat = models.CharField(max_length=10)
    token = models.CharField(max_length=255)
    qr_path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=now)