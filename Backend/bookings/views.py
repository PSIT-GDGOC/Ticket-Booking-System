from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from events.models import Event

from .services import SeatUnavailableError, book_seats


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
