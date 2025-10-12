from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event', 'seat']  # ✅ 'user' removed
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'seat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A3'}),
        }