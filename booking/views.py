from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Booking, Event, DownloadLog
from .forms import BookingForm, RegisterForm
from django.contrib import messages
from .utils import generate_token, generate_qr, generate_ticket_pdf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.utils import timezone

def index(request):
    return render(request, 'booking/index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'booking/login.html')

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'booking/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required
def book_ticket(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            existing = Booking.objects.filter(event=booking.event, seat=booking.seat).exists()
            if existing:
                messages.error(request, "Seat already booked for this event.")
                return redirect('book_ticket')

            booking.token = generate_token(request.user.id, booking.event.id, booking.seat)
            booking.qr_path = generate_qr(booking.token)
            booking.save()

            messages.success(request, "Ticket booked successfully!")
            return redirect('dashboard')
    else:
        form = BookingForm()
    return render(request, 'booking/booking.html', {'form': form})

@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/dashboard.html', {'bookings': bookings})

@login_required
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.user != request.user:
        messages.error(request, "You are not authorized to download this ticket.")
        return redirect('dashboard')

    if booking.download_count >= 3:
        messages.error(request, "Download limit reached. You can only download this ticket 3 times.")
        return redirect('dashboard')

    pdf_buffer = generate_ticket_pdf(booking)

    booking.download_count += 1
    booking.last_downloaded = timezone.now()
    booking.save()

    ip_address = request.META.get('REMOTE_ADDR')
    DownloadLog.objects.create(booking=booking, ip_address=ip_address)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking.seat}_{booking.event.title}.pdf"'
    return response