from datetime import timedelta
from unittest import mock

from django.contrib.auth.models import User
from django.core import mail
from django.db import transaction
from django.test import TestCase, TransactionTestCase
from django.utils import timezone

from events.models import Event, Seat

from .emails import (
    build_booking_confirmation,
    send_booking_confirmation,
)
from .models import Booking, BookingSeat


def make_booking(email="asha@example.com", seat_numbers=("A1", "A2"), status="CONFIRMED"):
    user = User.objects.create_user("asha", email=email, password="pw")
    event = Event.objects.create(
        title="Live Music Night",
        description="Music",
        venue="Town Hall, Kanpur",
        date_time=timezone.now() + timedelta(days=7),
        price=499,
    )
    booking = Booking.objects.create(user=user, event=event, total_amount=499 * len(seat_numbers), status=status)
    for number in seat_numbers:
        seat = Seat.objects.create(event=event, seat_number=number)
        BookingSeat.objects.create(booking=booking, seat=seat)
    return booking


class ConfirmationEmailTests(TestCase):
    def test_email_contains_accurate_booking_details(self):
        booking = make_booking()
        self.assertTrue(send_booking_confirmation(booking))

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, ["asha@example.com"])
        for text in (message.body, message.alternatives[0].content):
            self.assertIn(f"BK-{booking.pk:06d}", text)
            self.assertIn("Live Music Night", text)
            self.assertIn("Town Hall, Kanpur", text)
            self.assertIn("A1, A2", text)
            self.assertIn("998", text)
        self.assertIn("Live Music Night", message.subject)

    def test_seats_omitted_when_booking_has_none(self):
        booking = make_booking(seat_numbers=())
        self.assertNotIn("Seats:", build_booking_confirmation(booking).body)

    def test_user_without_email_is_skipped(self):
        booking = make_booking(email="")
        self.assertFalse(send_booking_confirmation(booking))
        self.assertEqual(len(mail.outbox), 0)

    def test_delivery_error_does_not_raise_or_change_booking(self):
        booking = make_booking()
        with mock.patch(
            "bookings.emails.EmailMultiAlternatives.send", side_effect=OSError("SMTP down")
        ):
            with self.assertLogs("bookings.emails", level="ERROR"):
                self.assertFalse(send_booking_confirmation(booking))
        booking.refresh_from_db()
        self.assertEqual(booking.status, "CONFIRMED")


class SendOnCommitTests(TransactionTestCase):
    """New bookings email the user automatically (see signals.py)."""

    def test_sent_once_after_commit(self):
        with transaction.atomic():
            make_booking()
            self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("A1, A2", mail.outbox[0].body)

    def test_not_sent_when_transaction_rolls_back(self):
        try:
            with transaction.atomic():
                make_booking()
                raise RuntimeError("seat already taken")
        except RuntimeError:
            pass
        self.assertEqual(len(mail.outbox), 0)

    def test_updating_a_booking_does_not_send_another_email(self):
        with transaction.atomic():
            booking = make_booking()
        booking.status = "CANCELLED"
        booking.save()
        self.assertEqual(len(mail.outbox), 1)

    def test_cancelled_booking_sends_nothing(self):
        with transaction.atomic():
            make_booking(status="CANCELLED")
        self.assertEqual(len(mail.outbox), 0)
