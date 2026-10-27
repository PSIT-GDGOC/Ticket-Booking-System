from datetime import timedelta

from django.contrib.admin import helpers
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from bookings.models import Booking, BookingSeat

from .models import Event, Seat


class AdminTestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_superuser("admin", "admin@example.com", "pw")
        cls.event = Event.objects.create(
            title="Live Music Night",
            description="Music",
            venue="Town Hall",
            date_time=timezone.now() + timedelta(days=5),
            price=300,
        )

    def setUp(self):
        self.client.force_login(self.admin_user)


class EventAdminTests(AdminTestBase):
    def test_changelist_shows_seat_counts(self):
        seats = [Seat.objects.create(event=self.event, seat_number=n) for n in ("A1", "A2", "A3")]
        booking = Booking.objects.create(user=self.admin_user, event=self.event, total_amount=300)
        BookingSeat.objects.create(booking=booking, seat=seats[0])

        response = self.client.get(reverse("admin:events_event_changelist"))

        self.assertEqual(response.status_code, 200)
        row = response.context["cl"].result_list[0]
        self.assertEqual((row._total_seats, row._booked_seats), (3, 1))

    def test_cancelled_booking_frees_the_seat_in_counts(self):
        seat = Seat.objects.create(event=self.event, seat_number="A1")
        booking = Booking.objects.create(
            user=self.admin_user, event=self.event, total_amount=300, status="CANCELLED"
        )
        BookingSeat.objects.create(booking=booking, seat=seat)

        response = self.client.get(reverse("admin:events_event_changelist"))

        self.assertEqual(response.context["cl"].result_list[0]._booked_seats, 0)

    def test_deactivate_action(self):
        self.client.post(
            reverse("admin:events_event_changelist"),
            {"action": "deactivate_events", helpers.ACTION_CHECKBOX_NAME: [self.event.pk]},
        )
        self.event.refresh_from_db()
        self.assertFalse(self.event.is_active)

    def test_generate_seats_shows_form_first(self):
        response = self.client.post(
            reverse("admin:events_event_changelist"),
            {"action": "generate_seats", helpers.ACTION_CHECKBOX_NAME: [self.event.pk]},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Generate seats for Live Music Night")
        self.assertEqual(self.event.seats.count(), 0)

    def test_generate_seats_creates_grid(self):
        response = self.client.post(
            reverse("admin:events_event_changelist"),
            {
                "action": "generate_seats",
                "apply": "1",
                "rows": 3,
                "seats_per_row": 4,
                helpers.ACTION_CHECKBOX_NAME: [self.event.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        numbers = set(self.event.seats.values_list("seat_number", flat=True))
        self.assertEqual(len(numbers), 12)
        self.assertEqual({"A1", "A4", "C1", "C4"} & numbers, {"A1", "A4", "C1", "C4"})

    def test_generate_seats_keeps_existing_seats(self):
        existing = Seat.objects.create(event=self.event, seat_number="A1")
        self.client.post(
            reverse("admin:events_event_changelist"),
            {
                "action": "generate_seats",
                "apply": "1",
                "rows": 1,
                "seats_per_row": 3,
                helpers.ACTION_CHECKBOX_NAME: [self.event.pk],
            },
        )
        self.assertEqual(self.event.seats.count(), 3)
        self.assertTrue(Seat.objects.filter(pk=existing.pk).exists())

    def test_generate_seats_rejects_invalid_size(self):
        response = self.client.post(
            reverse("admin:events_event_changelist"),
            {
                "action": "generate_seats",
                "apply": "1",
                "rows": 27,
                "seats_per_row": 0,
                helpers.ACTION_CHECKBOX_NAME: [self.event.pk],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.event.seats.count(), 0)

    def test_generate_seats_requires_exactly_one_event(self):
        other = Event.objects.create(
            title="Other", description="x", venue="y", date_time=timezone.now(), price=1
        )
        response = self.client.post(
            reverse("admin:events_event_changelist"),
            {"action": "generate_seats", helpers.ACTION_CHECKBOX_NAME: [self.event.pk, other.pk]},
            follow=True,
        )
        self.assertContains(response, "Select exactly one event")


class SeatAdminTests(AdminTestBase):
    def test_changelist_and_search_work(self):
        Seat.objects.create(event=self.event, seat_number="B7")
        url = reverse("admin:events_seat_changelist")

        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.get(url, {"q": "Live Music"})
        self.assertEqual(len(response.context["cl"].result_list), 1)
