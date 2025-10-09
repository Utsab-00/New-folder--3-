from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Booking, Event, User
from .forms import BookingForm
from .utils import generate_token, generate_qr
def index(request):
    return render(request, 'booking/index.html')


def book_ticket(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(id=form.cleaned_data['user_id'])
            except ObjectDoesNotExist:
                return render(request, 'booking/index.html', {
                    'form': form,
                    'error': 'User not found. Please enter a valid User ID.'
                })

            try:
                event = Event.objects.get(id=form.cleaned_data['event_id'])
            except ObjectDoesNotExist:
                return render(request, 'booking/index.html', {
                    'form': form,
                    'error': 'Event not found. Please enter a valid Event ID.'
                })

            seat = form.cleaned_data['seat']
            token = generate_token(user.id, event.id, seat)
            qr_path = generate_qr(token)

            Booking.objects.create(
                user=user,
                event=event,
                seat=seat,
                token=token,
                qr_path=qr_path
            )

            return redirect('dashboard')

        else:
            return render(request, 'booking/index.html', {
                'form': form,
                'error': 'Form is invalid. Please check your input.'
            })

    return redirect('index')

def dashboard(request):
    bookings = Booking.objects.all()
    return render(request, 'booking/dashboard.html', {'bookings': bookings})