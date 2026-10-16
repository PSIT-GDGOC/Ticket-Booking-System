
from django.db import models
from django.contrib.auth.models import User
from events.models import Event, Seat


class Booking(models.Model):
    STATUS_CHOICES = [
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="CONFIRMED"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username}"


class BookingSeat(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="booking_seats"
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.PROTECT,
        related_name="booking_records"
    )
    # Set to False when the booking is cancelled, so the seat is free again.
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["booking", "seat"],
                name="unique_seat_per_booking"
            ),
            # A seat can only have one active booking at a time.
            models.UniqueConstraint(
                fields=["seat"],
                condition=models.Q(is_active=True),
                name="unique_active_booking_per_seat"
            ),
        ]

    def __str__(self):
        return f"{self.booking} - {self.seat}"
