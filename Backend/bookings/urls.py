from django.urls import path

from . import views

urlpatterns = [
    path("book/<int:event_id>/", views.book_event_seats, name="book_seats"),
    path(
        "cancel/<int:booking_id>/",
        views.cancel_booking,
        name="cancel_booking",
    ),
]
