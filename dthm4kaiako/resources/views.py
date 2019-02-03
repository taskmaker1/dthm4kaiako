"""Views for resource application."""

from django.views import generic
from utils.mixins import RedirectToCosmeticURLMixin
from resources.models import (
    Resource,
)


class ResourceListView(generic.ListView):
    """View for listing resources."""

    model = Resource
    context_object_name = 'resources'


class ResourceDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for a resource."""

    model = Resource
    context_object_name = 'resource'

    def get_context_data(self, **kwargs):
        """Provide the context data for the resource detail view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['components'] = self.object.components.order_by('name')
        return context
