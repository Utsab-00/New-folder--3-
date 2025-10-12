import uuid
from datetime import datetime, timezone
import qrcode
import os
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def generate_token(user_id, event_id, seat):
    utc_time = datetime.now(timezone.utc).isoformat()
    return f"{uuid.uuid4()}|{user_id}|{event_id}|{seat}|{utc_time}"

def generate_qr(token):
    qr = qrcode.make(token)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f"{token}.png")

def generate_ticket_pdf(booking):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(width / 2, height - 1 * inch, "FairBook Ticket")

    pdf.setFont("Helvetica", 12)
    y_position = height - 2 * inch

    pdf.drawString(1 * inch, y_position, f"Event: {booking.event.title}")
    y_position -= 0.3 * inch
    pdf.drawString(1 * inch, y_position, f"Seat: {booking.seat}")
    y_position -= 0.3 * inch
    pdf.drawString(1 * inch, y_position, f"Token: {booking.token}")
    y_position -= 0.5 * inch

    if booking.qr_path:
        qr_img = ImageReader(booking.qr_path.path)
        pdf.drawImage(qr_img, 1 * inch, y_position - 2 * inch, width=2 * inch, height=2 * inch)

    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawCentredString(width / 2, 0.5 * inch, "Thank you for booking!")

    pdf.save()
    buffer.seek(0)
    return buffer
