
from django.contrib import admin
from .models import Booking, BookingSeat


class BookingSeatInline(admin.TabularInline):
    model = BookingSeat
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "total_amount", "status", "created_at")
    list_filter = ("status", "event", "created_at")
    search_fields = ("user__username", "event__title")
    inlines = [BookingSeatInline]


@admin.register(BookingSeat)
class BookingSeatAdmin(admin.ModelAdmin):
    list_display = ("booking", "seat")
    search_fields = ("booking__user__username", "seat__seat_number")
