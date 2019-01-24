"""Views for DTTA application."""

from django.views import generic
from django.utils import timezone
from dtta.models import (
    Page,
    NewsArticle,
)


class HomeView(generic.base.TemplateView):
    """View for DTTA homepage."""

    template_name = 'dtta/home.html'


class AboutView(generic.base.TemplateView):
    """View for DTTA about page."""

    template_name = 'dtta/about.html'


class MembershipView(generic.base.TemplateView):
    """View for DTTA membership page."""

    template_name = 'dtta/membership.html'


class PageDetailView(generic.DetailView):
    """View for DTTA flat page."""

    model = Page
    context_object_name = 'page'


class NewsArticleListView(generic.ListView):
    """View for listing DTTA news articles."""

    model = NewsArticle
    context_object_name = 'news_articles'
    queryset = NewsArticle.objects.filter(datetime__lte=timezone.now()).order_by('-datetime')


class NewsArticleDetailView(generic.DetailView):
    """View for DTTA news article."""

    model = NewsArticle
    context_object_name = 'news_article'