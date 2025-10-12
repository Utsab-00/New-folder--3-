# FairBook Setup Guide

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

4. Create some events via Django admin:
```bash
python manage.py runserver
# Visit http://localhost:8000/admin
# Login and create Event objects
```

5. Start the development server:
```bash
python manage.py runserver
```

## Features Implemented

### Authentication
- User registration with email
- Login/logout functionality
- Protected routes requiring authentication

### Ticket Booking
- Book tickets for events with seat selection
- Automatic QR code generation
- Unique seat constraint per event
- User-specific bookings

### PDF Ticket Generation
- Download tickets as PDF with embedded QR code
- Professional layout with event details
- Custom header and footer

### Download Tracking
- 3-download limit per ticket
- Download count and timestamp tracking
- IP address logging for audit trail
- Status indicators in dashboard

### Dashboard
- View all user bookings
- Download status display
- QR code preview
- Download PDF button

## Security Notes

For production deployment:
1. Change SECRET_KEY in settings.py
2. Set DEBUG = False
3. Configure ALLOWED_HOSTS
4. Use environment variables for sensitive data
5. Set up HTTPS
