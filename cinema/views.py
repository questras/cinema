from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db.models import Q

from .models import Showing, Movie


class ScheduleView(ListView):
    template_name = 'cinema/schedule.html'
    model = Showing
    context_object_name = 'showings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date().weekday()
        weekdays = (
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        )
        weekdays = weekdays[today:7] + weekdays[0:today]
        context['weekdays'] = weekdays

        return context

    def get_queryset(self):
        today = timezone.now()
        last_day = (today + timezone.timedelta(days=6)).replace(hour=23, minute=59)

        showings = Showing.objects.filter(
            when__gte=today,
            when__lte=last_day).order_by('when')
        return showings


class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'cinema/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        movie = self.get_object()
        now = timezone.now()
        showings = movie.showing_set.filter(when__gte=now).order_by('when')
        context['showings'] = showings

        return context


class ShowingDetailView(DetailView):
    model = Showing
    context_object_name = 'showing'
    template_name = 'cinema/showing_detail.html'


class MovieListView(ListView):
    model = Movie
    template_name = 'cinema/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        search_query = self.request.GET.get('search_query') or None

        if search_query:
            queryset = Movie.objects.filter(
                Q(title__icontains=search_query) | Q(director__icontains=search_query)
            )
        else:
            queryset = Movie.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        search_query = self.request.GET.get('search_query') or ''

        context['search_query'] = search_query

        return context
