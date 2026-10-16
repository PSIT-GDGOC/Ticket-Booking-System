import threading
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import IntegrityError, OperationalError, connection, transaction
from django.test import Client, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from events.models import Event, Seat

from .models import Booking, BookingSeat
from .services import SeatUnavailableError, book_seats, cancel_booking


class BookingTestBase(TransactionTestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title="Concert",
            description="Live",
            venue="Hall",
            date_time=timezone.now() + timedelta(days=7),
            price="500.00",
        )
        self.seat_a = Seat.objects.create(event=self.event, seat_number="A1")
        self.seat_b = Seat.objects.create(event=self.event, seat_number="A2")
        self.alice = User.objects.create_user("alice", password="pw")
        self.bob = User.objects.create_user("bob", password="pw")


class DoubleBookingTests(BookingTestBase):
    def test_booking_available_seat_succeeds(self):
        booking = book_seats(self.alice, self.event, [self.seat_a.pk, self.seat_b.pk])
        self.assertEqual(booking.booking_seats.count(), 2)
        self.assertEqual(str(booking.total_amount), "1000.00")

    def test_already_booked_seat_cannot_be_booked_again(self):
        book_seats(self.alice, self.event, [self.seat_a.pk])
        with self.assertRaises(SeatUnavailableError):
            book_seats(self.bob, self.event, [self.seat_a.pk])
        self.assertEqual(Booking.objects.count(), 1)

    def test_failed_multi_seat_booking_is_all_or_nothing(self):
        book_seats(self.alice, self.event, [self.seat_a.pk])
        with self.assertRaises(SeatUnavailableError):
            book_seats(self.bob, self.event, [self.seat_a.pk, self.seat_b.pk])
        self.assertEqual(Booking.objects.filter(user=self.bob).count(), 0)
        self.assertFalse(BookingSeat.objects.filter(seat=self.seat_b).exists())

    def test_seat_from_another_event_is_rejected(self):
        other = Event.objects.create(
            title="Other", description="x", venue="y",
            date_time=timezone.now() + timedelta(days=1), price="1.00",
        )
        foreign_seat = Seat.objects.create(event=other, seat_number="Z1")
        with self.assertRaises(SeatUnavailableError):
            book_seats(self.alice, self.event, [foreign_seat.pk])

    def test_cannot_book_too_many_seats_at_once(self):
        with self.assertRaises(SeatUnavailableError):
            book_seats(self.alice, self.event, range(1, 12))

    def test_cancelled_seat_can_be_rebooked(self):
        booking = book_seats(self.alice, self.event, [self.seat_a.pk])
        cancel_booking(booking)
        book_seats(self.bob, self.event, [self.seat_a.pk])
        self.assertEqual(
            BookingSeat.objects.filter(seat=self.seat_a, is_active=True).count(), 1
        )

    def test_database_constraint_blocks_duplicate_active_rows(self):
        book_seats(self.alice, self.event, [self.seat_a.pk])
        rogue = Booking.objects.create(user=self.bob, event=self.event, total_amount=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            BookingSeat.objects.create(booking=rogue, seat=self.seat_a)

    def test_view_shows_error_when_seat_unavailable(self):
        book_seats(self.alice, self.event, [self.seat_a.pk])
        client = Client()
        client.force_login(self.bob)
        response = client.post(
            reverse("book_seats", args=[self.event.pk]),
            {"seats": [self.seat_a.pk]},
            follow=True,
        )
        msgs = [str(m) for m in response.context["messages"]]
        self.assertTrue(any("no longer available" in m for m in msgs))
        self.assertEqual(Booking.objects.filter(user=self.bob).count(), 0)


class ConcurrentBookingTests(BookingTestBase):
    def test_simultaneous_requests_book_a_seat_only_once(self):
        users = [User.objects.create_user(f"u{i}", password="pw") for i in range(10)]
        barrier = threading.Barrier(len(users))
        outcomes = []

        def attempt(user):
            try:
                barrier.wait()
                book_seats(user, self.event, [self.seat_a.pk])
                outcomes.append("booked")
            except SeatUnavailableError:
                outcomes.append("rejected")
            except OperationalError:
                # SQLite sometimes says "table is locked" when threads write
                # together. That request didn't book anything, so it's fine.
                outcomes.append("locked")
            except Exception as exc:
                outcomes.append(f"error: {exc!r}")
            finally:
                connection.close()  # each thread has its own connection

        threads = [threading.Thread(target=attempt, args=(u,)) for u in users]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(outcomes.count("booked"), 1, outcomes)
        self.assertEqual(
            outcomes.count("rejected") + outcomes.count("locked"),
            len(users) - 1,
            outcomes,
        )
        self.assertEqual(
            BookingSeat.objects.filter(seat=self.seat_a, is_active=True).count(), 1
        )
