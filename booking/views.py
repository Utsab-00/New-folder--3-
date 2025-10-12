from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Booking, Event, DownloadLog
from .forms import BookingForm
from .utils import generate_token, generate_qr
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .decorators import staff_required

@staff_required
def index(request):
    form = BookingForm()
    return render(request, 'booking/index.html', {'form': form})

@staff_required
def book_ticket(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            if Booking.objects.filter(event=booking.event, seat=booking.seat).exists():
                messages.error(request, "❌ Seat already booked for this event.")
                return redirect('index')

            booking.token = generate_token(request.user, booking.event, booking.seat)
            booking.qr_path = generate_qr(booking.token)
            booking.save()

            messages.success(request, "✅ Ticket booked successfully!")
            return redirect('dashboard')
    else:
        messages.error(request, "⚠️ Invalid form submission.")
        print(form.errors)  # 👈 Add this for debugging
        form = BookingForm()
    return render(request, 'booking/index.html', {'form': form})

@staff_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/dashboard.html', {'bookings': bookings})

@staff_required
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.user != request.user:
        messages.error(request, "⛔ Unauthorized access.")
        return redirect('dashboard')

    if booking.download_count >= 3:
        messages.error(request, "⚠️ Download limit exceeded.")
        return redirect('dashboard')

    DownloadLog.objects.create(
        booking=booking,
        user=request.user,
        ip_address=request.META.get('REMOTE_ADDR', 'unknown')
    )

    booking.downloaded = True
    booking.download_count += 1
    booking.last_downloaded_at = timezone.now()
    booking.save()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Ticket_{booking.token}.pdf'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # 🎟️ Header
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - 80, "🎟️ FairBook Ticket")

    # 👤 User Name
    user_name = booking.user.get_full_name() or booking.user.username
    p.setFont("Helvetica", 12)
    p.drawString(80, height - 130, f"Name: {user_name}")

    # 📅 Event Details
    p.drawString(80, height - 150, f"Event: {booking.event.title}")
    p.drawString(80, height - 170, f"Date: {booking.event.date.strftime('%d %b %Y, %I:%M %p')}")
    p.drawString(80, height - 190, f"Location: {booking.event.location}")

    # 🪑 Booking Info
    p.drawString(80, height - 210, f"Seat: {booking.seat}")
    p.drawString(80, height - 230, f"Token: {booking.token}")

    # 🖼️ QR Code
    if booking.qr_path and booking.qr_path.path:
        try:
            p.drawImage(booking.qr_path.path, width - 180, height - 280, width=100, height=100)
        except Exception:
            p.drawString(80, height - 250, "QR Code could not be loaded.")
    else:
        p.drawString(80, height - 250, "QR Code not available.")

    # 🕒 Timestamp
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(80, 60, f"Generated on: {booking.timestamp.strftime('%d %b %Y, %I:%M %p')}")

    # 🏷️ Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width / 2, 40, "Thank you for booking with FairBook!")

    p.showPage()
    p.save()

    return response

@staff_required
def preview_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/ticket_template.html', {'booking': booking})