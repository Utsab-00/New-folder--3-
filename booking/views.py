from django.shortcuts import render, redirect
from .models import Booking, Event, User
from .forms import BookingForm
from .utils import generate_token, generate_qr

def index(request):
    return render(request, 'booking/index.html')

def book_ticket(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=form.cleaned_data['user_id'])
            event = Event.objects.get(id=form.cleaned_data['event_id'])
            seat = form.cleaned_data['seat']
            token = generate_token(user.id, event.id, seat)
            qr_path = generate_qr(token)
            Booking.objects.create(user=user, event=event, seat=seat, token=token, qr_path=qr_path)
            return redirect('dashboard')
    return render(request, 'booking/booking.html')

def dashboard(request):
    bookings = Booking.objects.all()
    return render(request, 'booking/dashboard.html', {'bookings': bookings})