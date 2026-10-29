from decimal import Decimal

from django.db import IntegrityError, transaction

from events.models import Seat

from .models import Booking, BookingSeat

MAX_SEATS_PER_BOOKING = 10


class SeatUnavailableError(Exception):
    """Raised when a seat can't be booked (already taken, invalid, etc.)."""


def book_seats(user, event, seat_ids):
    """Book the given seats for the user, or book nothing at all."""
    seat_ids = {int(i) for i in seat_ids}

    if not seat_ids:
        raise SeatUnavailableError("Please select at least one seat.")
    if len(seat_ids) > MAX_SEATS_PER_BOOKING:
        raise SeatUnavailableError(
            f"You can book at most {MAX_SEATS_PER_BOOKING} seats at a time."
        )

    try:
        with transaction.atomic():
            # Lock the rows while we check them. SQLite ignores this, but
            # PostgreSQL/MySQL use it. Sorting by id avoids deadlocks.
            seats = list(
                Seat.objects.select_for_update()
                .filter(event=event, pk__in=seat_ids)
                .order_by("pk")
            )
            if len(seats) != len(seat_ids):
                raise SeatUnavailableError("Some of the selected seats are invalid.")

            taken = BookingSeat.objects.filter(
                seat__in=seats, is_active=True
            ).values_list("seat__seat_number", flat=True)
            if taken:
                raise SeatUnavailableError(
                    f"Seat(s) {', '.join(sorted(taken))} are no longer available. "
                    "Please choose another seat."
                )

            booking = Booking.objects.create(
                user=user,
                event=event,
                total_amount=Decimal(event.price) * len(seats),
            )
            BookingSeat.objects.bulk_create(
                BookingSeat(booking=booking, seat=seat) for seat in seats
            )
            return booking
    except IntegrityError:
        # Someone else booked the seat between our check and the insert.
        # The database constraint stopped it, so just tell the user.
        raise SeatUnavailableError(
            "Someone just booked one of those seats. Please choose another seat."
        )


def cancel_booking(booking):
    """Cancel a booking and free its seats.

    Note: the caller must check that the booking belongs to the user.
    """
    with transaction.atomic():
        booking = Booking.objects.select_for_update().get(pk=booking.pk)
        if booking.status == "CANCELLED":
            return booking
        booking.status = "CANCELLED"
        booking.save(update_fields=["status"])
        booking.booking_seats.update(is_active=False)
        return booking
