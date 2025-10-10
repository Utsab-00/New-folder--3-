from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Booking, Event, User
from .forms import BookingForm
from django.contrib import messages
from .utils import generate_token, generate_qr
def index(request):
    return render(request, 'booking/index.html')


def book_ticket(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.token = generate_token(booking.user, booking.event, booking.seat)
            booking.qr_path = generate_qr(booking.token)
            booking.save()
            messages.success(request, "✅ Ticket booked successfully!")
            return redirect('dashboard')
    else:
        form = BookingForm()
    return render(request, 'booking/index.html', {'form': form})


def dashboard(request):
    bookings = Booking.objects.all()
    return render(request, 'booking/dashboard.html', {'bookings': bookings})