"""Views for events application."""

from django.views import generic
from django.utils.timezone import now
from utils.mixins import RedirectToCosmeticURLMixin
from events.models import (
    Event,
)


class HomeView(generic.TemplateView):
    """View for event homepage."""

    template_name = 'events/home.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the event homepage view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        future_events = Event.objects.filter(published=True).filter(end__gte=now()).order_by('start').prefetch_related(
            'organisers',
            'locations',
            'sponsors',
        ).select_related(
            'series',
        )
        # Force evaluation of queryset
        future_events = list(future_events)
        context['events'] = future_events[:10]

        raw_map_locations = {}
        for event in future_events:
            for location in event.locations.all():
                key = location.pk
                if location.pk not in raw_map_locations:
                    # Create basic location information
                    raw_map_locations[key] = {
                        'coords': {'lat': location.coords.y, 'lng': location.coords.x},
                        'title': location.name,
                        'text': '<div class="map-info-title">{}</div>'.format(location.name),
                    }
                raw_map_locations[key]['text'] += '<p class="mb-0"><a href="{}">{:%-d %b %Y} - {}</a></p>'.format(
                    event.get_absolute_url(),
                    event.start,
                    event.name
                )
        context['raw_map_locations'] = list(raw_map_locations.values())
        return context


class EventListView(generic.ListView):
    """View for listing events."""

    model = Event
    context_object_name = 'events'

    def get_queryset(self):
        """Only show published events.

        Returns:
            Events filtered by published boolean.
        """
        return Event.objects.filter(published=True).order_by('start').prefetch_related(
            'organisers',
            'locations',
            'sponsors',
        ).select_related(
            'series',
        )


class EventDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for a specific event."""

    model = Event
    context_object_name = 'event'

    def get_queryset(self):
        """Only show published events.

        Returns:
            Events filtered by published boolean.
        """
        return Event.objects.filter(published=True).prefetch_related('locations')

    def get_context_data(self, **kwargs):
        """Provide the context data for the event view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['sponsors'] = self.object.sponsors.all()
        context['organisers'] = self.object.organisers.all()
        context['sessions'] = self.object.sessions.all().prefetch_related('locations')
        if self.object.locations.count() == 1:
            context['location'] = self.object.locations.first()
        elif self.object.locations.count() > 1:
            context['locations'] = self.object.locations.all()
        return context
