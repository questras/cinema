from django.views.generic import ListView, DetailView, TemplateView
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages

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


class ShowingListView(TemplateView):
    template_name = 'cinema/showing_list.html'

    def get_context_data(self, **kwargs):
        context = super(ShowingListView, self).get_context_data(**kwargs)

        movie = self.request.GET.get('movie') or ''
        from_when = self.request.GET.get('from_when') or ''
        to_when = self.request.GET.get('to_when') or ''

        now = timezone.localtime(timezone.now())
        if from_when:
            try:
                from_when = timezone.make_aware(timezone.datetime.strptime(from_when, '%d/%m/%Y %H:%M'))
                from_when = max(from_when, now)  # Make sure from_when is at least now.
            except ValueError:
                messages.error(self.request, message='An incorrect date was provided.')
                return context
        else:
            from_when = now

        if to_when:
            try:
                to_when = timezone.make_aware(timezone.datetime.strptime(to_when, '%d/%m/%Y %H:%M'))
            except ValueError:
                messages.error(self.request, message='An incorrect date was provided.')
                return context

        showings = Showing.objects.filter(
            (Q(movie__title__icontains=movie) | Q(movie__director__icontains=movie)),
            Q(when__gte=from_when)
        )

        if to_when:
            showings = showings.filter(Q(when__lte=to_when))

        context['movie'] = movie
        if to_when:
            context['to_when'] = timezone.datetime.strftime(to_when, '%d/%m/%Y %H:%M')
        context['from_when'] = timezone.datetime.strftime(from_when, '%d/%m/%Y %H:%M')
        context['showings'] = showings

        return context
