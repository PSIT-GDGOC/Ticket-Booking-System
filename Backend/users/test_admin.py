from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from bookings.models import Booking
from events.models import Event

ADMIN_PAGES = [
    "admin:index",
    "admin:auth_user_changelist",
    "admin:events_event_changelist",
    "admin:events_seat_changelist",
    "admin:bookings_booking_changelist",
    "admin:bookings_bookingseat_changelist",
]


class AdminAccessTests(TestCase):
    """Only active staff members may use the admin panel."""

    @classmethod
    def setUpTestData(cls):
        cls.customer = User.objects.create_user("asha", password="pw")
        cls.staff_without_perms = User.objects.create_user("clerk", password="pw", is_staff=True)
        cls.superuser = User.objects.create_superuser("admin", "admin@example.com", "pw")

    def test_anonymous_users_are_sent_to_login(self):
        for name in ADMIN_PAGES:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 302)
                self.assertIn("/admin/login/", response["Location"])

    def test_regular_users_cannot_use_admin(self):
        self.client.force_login(self.customer)
        for name in ADMIN_PAGES:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 302)
                self.assertIn("/admin/login/", response["Location"])

    def test_staff_without_permissions_cannot_manage_data(self):
        self.client.force_login(self.staff_without_perms)
        for name in ADMIN_PAGES[1:]:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 403)

    def test_superuser_can_open_every_page(self):
        self.client.force_login(self.superuser)
        for name in ADMIN_PAGES:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_public_site_still_works_for_anonymous_visitors(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)


class UserAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser("admin", "admin@example.com", "pw")
        cls.customer = User.objects.create_user("asha", email="asha@example.com", password="pw")
        event = Event.objects.create(
            title="Live Music Night",
            description="Music",
            venue="Town Hall",
            date_time=timezone.now() + timedelta(days=3),
            price=100,
        )
        Booking.objects.create(user=cls.customer, event=event, total_amount=100)
        Booking.objects.create(user=cls.customer, event=event, total_amount=100)

    def setUp(self):
        self.client.force_login(self.superuser)

    def test_changelist_shows_booking_counts(self):
        response = self.client.get(reverse("admin:auth_user_changelist"))
        counts = {u.username: u._booking_count for u in response.context["cl"].result_list}
        self.assertEqual(counts["asha"], 2)
        self.assertEqual(counts["admin"], 0)

    def test_search_by_email(self):
        response = self.client.get(reverse("admin:auth_user_changelist"), {"q": "asha@example"})
        self.assertEqual([u.username for u in response.context["cl"].result_list], ["asha"])

    def test_user_change_page_loads(self):
        url = reverse("admin:auth_user_change", args=[self.customer.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
