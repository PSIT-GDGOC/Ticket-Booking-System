import string

from django import forms
from django.contrib import admin, messages
from django.db.models import Count, Q
from django.template.response import TemplateResponse

from .models import Event, Seat

admin.site.site_header = "Ticket Booking System Admin"
admin.site.site_title = "Ticket Booking Admin"
admin.site.index_title = "Manage events, seats and bookings"

# A seat counts as booked while it belongs to a CONFIRMED booking.
BOOKED_FILTER = Q(booking_records__booking__status="CONFIRMED")


class GenerateSeatsForm(forms.Form):
    """Asks how large the seat grid should be (rows A, B, C... by seat number)."""

    rows = forms.IntegerField(
        min_value=1,
        max_value=len(string.ascii_uppercase),
        help_text="Number of rows, labelled A, B, C... (maximum 26).",
    )
    seats_per_row = forms.IntegerField(
        min_value=1,
        max_value=100,
        help_text="Seats in each row, numbered 1, 2, 3... (for example A1, A2).",
    )


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "venue",
        "date_time",
        "price",
        "is_active",
        "total_seats",
        "booked_seats",
        "available_seats",
    )
    list_filter = ("is_active", "date_time")
    list_editable = ("is_active",)
    search_fields = ("title", "venue", "description")
    date_hierarchy = "date_time"
    ordering = ("-date_time",)
    readonly_fields = ("created_at",)
    inlines = [SeatInline]
    actions = ["activate_events", "deactivate_events", "generate_seats"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _total_seats=Count("seats", distinct=True),
            _booked_seats=Count(
                "seats", filter=Q(seats__booking_records__booking__status="CONFIRMED"), distinct=True
            ),
        )

    @admin.display(description="Seats", ordering="_total_seats")
    def total_seats(self, obj):
        return obj._total_seats

    @admin.display(description="Booked", ordering="_booked_seats")
    def booked_seats(self, obj):
        return obj._booked_seats

    @admin.display(description="Available")
    def available_seats(self, obj):
        return obj._total_seats - obj._booked_seats

    @admin.action(description="Activate selected events")
    def activate_events(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} event(s) activated.", messages.SUCCESS)

    @admin.action(description="Deactivate selected events")
    def deactivate_events(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} event(s) deactivated.", messages.SUCCESS)

    @admin.action(description="Generate seat grid for selected event")
    def generate_seats(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Select exactly one event to generate seats for.", messages.ERROR)
            return None
        event = queryset.get()

        if "apply" in request.POST:
            form = GenerateSeatsForm(request.POST)
            if form.is_valid():
                existing = set(event.seats.values_list("seat_number", flat=True))
                new_seats = [
                    Seat(event=event, seat_number=f"{row}{number}")
                    for row in string.ascii_uppercase[: form.cleaned_data["rows"]]
                    for number in range(1, form.cleaned_data["seats_per_row"] + 1)
                    if f"{row}{number}" not in existing
                ]
                Seat.objects.bulk_create(new_seats)
                self.message_user(
                    request,
                    f"Created {len(new_seats)} seat(s) for {event.title}; "
                    f"{len(existing)} existing seat(s) were left untouched.",
                    messages.SUCCESS,
                )
                return None
        else:
            form = GenerateSeatsForm()

        context = {
            **self.admin_site.each_context(request),
            "title": f"Generate seats for {event.title}",
            "opts": self.model._meta,
            "event": event,
            "form": form,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            "selected_pk": event.pk,
        }
        return TemplateResponse(request, "admin/events/event/generate_seats.html", context)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("seat_number", "event", "is_booked")
    list_filter = ("event",)
    list_select_related = ("event",)
    search_fields = ("seat_number", "event__title")
    ordering = ("event", "seat_number")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _booked_count=Count("booking_records", filter=BOOKED_FILTER, distinct=True)
        )

    @admin.display(description="Booked", boolean=True, ordering="_booked_count")
    def is_booked(self, obj):
        return obj._booked_count > 0
