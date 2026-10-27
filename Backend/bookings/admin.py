from django.contrib import admin, messages

from .models import Booking, BookingSeat


class BookingSeatInline(admin.TabularInline):
    model = BookingSeat
    extra = 0
    raw_id_fields = ("seat",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_reference", "user", "event", "seat_count", "total_amount", "status", "created_at")
    list_filter = ("status", "event", "created_at")
    list_select_related = ("user", "event")
    search_fields = ("user__username", "user__email", "event__title", "id")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    raw_id_fields = ("user", "event")
    inlines = [BookingSeatInline]
    actions = ["mark_cancelled"]

    def get_readonly_fields(self, request, obj=None):
        # Once a booking exists, its owner, event and amount must not be edited
        # by hand (they would no longer match the booked seats / what was paid).
        # Staff can still change the status, or add one when creating a booking.
        if obj is not None:
            return ("user", "event", "total_amount", "created_at")
        return ("created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("booking_seats")

    @admin.display(description="Reference")
    def booking_reference(self, obj):
        return f"BK-{obj.pk:06d}"

    @admin.display(description="Seats")
    def seat_count(self, obj):
        return len(obj.booking_seats.all())

    @admin.action(description="Mark selected bookings as cancelled")
    def mark_cancelled(self, request, queryset):
        updated = queryset.filter(status="CONFIRMED").update(status="CANCELLED")
        self.message_user(request, f"{updated} booking(s) cancelled.", messages.SUCCESS)


@admin.register(BookingSeat)
class BookingSeatAdmin(admin.ModelAdmin):
    list_display = ("booking", "seat")
    list_select_related = ("booking__user", "seat__event")
    search_fields = ("booking__user__username", "seat__seat_number", "seat__event__title")
    raw_id_fields = ("booking", "seat")
