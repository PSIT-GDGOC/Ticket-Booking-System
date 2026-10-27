from datetime import timedelta

from django.contrib.admin import helpers
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from events.models import Event, Seat

from .models import Booking, BookingSeat


class BookingAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_superuser("admin", "admin@example.com", "pw")
        cls.customer = User.objects.create_user("asha", email="asha@example.com", password="pw")
        cls.event = Event.objects.create(
            title="Live Music Night",
            description="Music",
            venue="Town Hall",
            date_time=timezone.now() + timedelta(days=5),
            price=300,
        )
        cls.booking = Booking.objects.create(user=cls.customer, event=cls.event, total_amount=600)
        for number in ("A1", "A2"):
            seat = Seat.objects.create(event=cls.event, seat_number=number)
            BookingSeat.objects.create(booking=cls.booking, seat=seat)

    def setUp(self):
        self.client.force_login(self.admin_user)

    def test_changelist_shows_reference_and_seat_count(self):
        response = self.client.get(reverse("admin:bookings_booking_changelist"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"BK-{self.booking.pk:06d}")
        admin_obj = response.context["cl"].model_admin
        self.assertEqual(admin_obj.seat_count(response.context["cl"].result_list[0]), 2)

    def test_search_by_customer_email(self):
        response = self.client.get(reverse("admin:bookings_booking_changelist"), {"q": "asha@example"})
        self.assertEqual(len(response.context["cl"].result_list), 1)

    def test_mark_cancelled_action(self):
        self.client.post(
            reverse("admin:bookings_booking_changelist"),
            {"action": "mark_cancelled", helpers.ACTION_CHECKBOX_NAME: [self.booking.pk]},
        )
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "CANCELLED")

    def test_amount_owner_and_event_are_read_only_once_booked(self):
        admin_obj = self.client.get(reverse("admin:bookings_booking_changelist")).context["cl"].model_admin
        readonly = admin_obj.get_readonly_fields(None, self.booking)
        for field in ("user", "event", "total_amount", "created_at"):
            self.assertIn(field, readonly)
        self.assertNotIn("status", readonly)

    def test_posting_changes_to_protected_fields_is_ignored(self):
        other_user = User.objects.create_user("other", password="pw")
        url = reverse("admin:bookings_booking_change", args=[self.booking.pk])
        self.client.post(
            url,
            {
                "user": other_user.pk,
                "event": self.event.pk,
                "total_amount": "1.00",
                "status": "CANCELLED",
                "booking_seats-TOTAL_FORMS": 0,
                "booking_seats-INITIAL_FORMS": 0,
            },
        )
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.user, self.customer)
        self.assertEqual(self.booking.total_amount, 600)
        self.assertEqual(self.booking.status, "CANCELLED")

    def test_fields_are_editable_when_adding_a_booking(self):
        admin_obj = self.client.get(reverse("admin:bookings_booking_changelist")).context["cl"].model_admin
        self.assertEqual(admin_obj.get_readonly_fields(None, None), ("created_at",))

    def test_change_page_loads(self):
        url = reverse("admin:bookings_booking_change", args=[self.booking.pk])
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_booking_seat_changelist_loads(self):
        self.assertEqual(self.client.get(reverse("admin:bookings_bookingseat_changelist")).status_code, 200)
