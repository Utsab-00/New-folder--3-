from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event', 'seat']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'seat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A3'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'