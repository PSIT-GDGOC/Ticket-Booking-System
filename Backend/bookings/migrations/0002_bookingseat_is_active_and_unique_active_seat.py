from django.db import migrations, models


def reconcile_active_booking_seats(apps, schema_editor):
    """Keep the oldest active record for each seat before enforcing uniqueness."""
    BookingSeat = apps.get_model("bookings", "BookingSeat")
    BookingSeat.objects.filter(booking__status="CANCELLED").update(is_active=False)

    seat_ids = (
        BookingSeat.objects.filter(is_active=True)
        .values_list("seat_id", flat=True)
        .distinct()
    )
    for seat_id in seat_ids.iterator():
        duplicate_ids = list(
            BookingSeat.objects.filter(seat_id=seat_id, is_active=True)
            .order_by("id")
            .values_list("id", flat=True)[1:]
        )
        if duplicate_ids:
            BookingSeat.objects.filter(id__in=duplicate_ids).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookingseat",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(reconcile_active_booking_seats, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="bookingseat",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_active", True)),
                fields=("seat",),
                name="unique_active_booking_per_seat",
            ),
        ),
    ]
