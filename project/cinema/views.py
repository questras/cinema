from django.views.generic import ListView, DetailView
from django.utils import timezone

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
