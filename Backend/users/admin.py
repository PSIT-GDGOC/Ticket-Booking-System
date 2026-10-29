from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models import Count

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Django's user admin plus how many bookings each user has made."""

    list_display = BaseUserAdmin.list_display + ("date_joined", "booking_count")
    list_filter = BaseUserAdmin.list_filter + ("date_joined",)
    ordering = ("-date_joined",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_booking_count=Count("bookings", distinct=True))

    @admin.display(description="Bookings", ordering="_booking_count")
    def booking_count(self, obj):
        return obj._booking_count
