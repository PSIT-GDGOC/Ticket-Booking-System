from django.db import migrations, models


def deactivate_cancelled(apps, schema_editor):
    BookingSeat = apps.get_model("bookings", "BookingSeat")
    BookingSeat.objects.filter(booking__status="CANCELLED").update(is_active=False)


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
        migrations.RunPython(deactivate_cancelled, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="bookingseat",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_active", True)),
                fields=("seat",),
                name="unique_active_booking_per_seat",
            ),
        ),
    ]
