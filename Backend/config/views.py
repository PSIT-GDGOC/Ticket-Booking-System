
from django.shortcuts import render, get_object_or_404
from events.models import Event


def home(request):
    events = Event.objects.filter(is_active=True).order_by("date_time")
    return render(request, "home.html", {"events": events})


def event_detail(request, event_id):
    event = get_object_or_404(
        Event,
        id=event_id,
        is_active=True
    )
    return render(request, "event_detail.html", {"event": event})
