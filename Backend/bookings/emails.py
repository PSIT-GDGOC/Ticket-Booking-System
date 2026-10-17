import logging

from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def build_booking_confirmation(booking):
    """Build (but do not send) the confirmation email for a booking."""
    seats = [
        bs.seat.seat_number
        for bs in booking.booking_seats.select_related("seat").order_by("seat__seat_number")
    ]
    event = booking.event
    local_start = timezone.localtime(event.date_time)
    context = {
        "booking": booking,
        "booking_reference": f"BK-{booking.pk:06d}",
        "event": event,
        "event_date": local_start.strftime("%A, %d %B %Y"),
        "event_time": local_start.strftime("%I:%M %p %Z").lstrip("0"),
        "seats": seats,
        "user": booking.user,
    }
    html_body = render_to_string("bookings/email/booking_confirmation.html", context)
    text_body = render_to_string("bookings/email/booking_confirmation.txt", context)

    message = EmailMultiAlternatives(
        subject=f"Booking confirmed: {event.title} ({context['booking_reference']})",
        body=text_body or strip_tags(html_body),
        to=[booking.user.email],
    )
    message.attach_alternative(html_body, "text/html")
    return message


def send_booking_confirmation(booking):
    """Send the confirmation email. Never raises; returns True if it was sent.

    Email delivery problems are logged, but they must not affect the booking,
    which is already saved by the time this runs.
    """
    if not booking.user.email:
        logger.warning("Booking %s: user has no email address; skipping.", booking.pk)
        return False
    try:
        build_booking_confirmation(booking).send()
    except Exception:
        logger.exception("Booking %s: failed to send confirmation email.", booking.pk)
        return False
    return True


def send_booking_confirmation_on_commit(booking):
    """Schedule the email to go out only once the booking transaction commits.

    Called automatically by the post_save signal in signals.py when a confirmed
    booking is created, so do not call it again from views or services (that
    would send two emails). If the transaction rolls back, no email is sent.
    """
    transaction.on_commit(lambda: send_booking_confirmation(booking))
