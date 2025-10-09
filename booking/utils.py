import uuid
from datetime import datetime, timezone
import qrcode
import os

def generate_token(user_id, event_id, seat):
    utc_time = datetime.now(timezone.utc).isoformat()
    return f"{uuid.uuid4()}|{user_id}|{event_id}|{seat}|{utc_time}"

def generate_qr(token):
    img = qrcode.make(token)
    filename = f"{token[:8]}.png"
    path = os.path.join("static", "qr_codes", filename)
    img.save(path)
    return path