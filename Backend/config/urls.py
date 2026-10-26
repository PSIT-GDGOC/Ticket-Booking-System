from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path(
        "events/<int:event_id>/",
        views.event_detail,
        name="event_detail",
    ),
    path("", include("bookings.urls")),
]
