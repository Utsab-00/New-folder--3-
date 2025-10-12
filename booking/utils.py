import uuid
from datetime import datetime, timezone
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO

def generate_token(user, event, seat):
    utc_time = datetime.now(timezone.utc).isoformat()
    return f"{uuid.uuid4()}|{user.username}|{event.title}|{seat}|{utc_time}"

def generate_qr(token):
    qr = qrcode.make(token)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f"{uuid.uuid4()}.png")