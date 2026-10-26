from django.db.models.signals import post_save
from django.dispatch import receiver

from .emails import send_booking_confirmation_on_commit
from .models import Booking


@receiver(post_save, sender=Booking, dispatch_uid="booking_confirmation_email")
def email_confirmation_for_new_booking(sender, instance, created, raw=False, **kwargs):
    """Email the user once a new booking is safely saved.

    The email goes out only after the surrounding transaction commits, so a
    booking that is rolled back (for example because a seat was taken) never
    sends one. Create the booking and its seats inside one transaction
    (transaction.atomic) so the email can list the seats.
    """
    if raw or not created or instance.status != "CONFIRMED":
        return  # skip fixture loading, later edits and non-confirmed bookings
    send_booking_confirmation_on_commit(instance)
