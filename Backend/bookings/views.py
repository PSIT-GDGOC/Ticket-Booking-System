from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from events.models import Event

from .models import Booking
from .services import (
    SeatUnavailableError,
    book_seats,
    cancel_booking as cancel_booking_service,
)


@login_required
@require_POST
def book_event_seats(request, event_id):
    event = get_object_or_404(Event, pk=event_id, is_active=True)
    try:
        book_seats(request.user, event, request.POST.getlist("seats"))
    except ValueError:
        messages.error(request, "Invalid seat selection.")
    except SeatUnavailableError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "Booking confirmed!")
    return redirect("event_detail", event_id=event.pk)


@login_required
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        pk=booking_id,
        user=request.user,
    )
    cancel_booking_service(booking)
    messages.success(request, "Booking cancelled.")
    return redirect("event_detail", event_id=booking.event_id)
