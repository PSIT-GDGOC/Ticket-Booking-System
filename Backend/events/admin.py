
from django.contrib import admin
from .models import Event, Seat


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "venue", "date_time", "price", "is_active")
    list_filter = ("is_active", "date_time")
    search_fields = ("title", "venue")
    inlines = [SeatInline]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("seat_number", "event")
    list_filter = ("event",)
    search_fields = ("seat_number",)
