from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'event', 'seat']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
            'seat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A3'}),
        }