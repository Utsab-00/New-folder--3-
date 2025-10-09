from django import forms

class BookingForm(forms.Form):
    user_id = forms.IntegerField()
    event_id = forms.IntegerField()
    seat = forms.CharField(max_length=10)