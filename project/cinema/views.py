from django.views.generic import ListView
from django.utils import timezone

from .models import Showing


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
        today = timezone.now().date()
        last_day = today + timezone.timedelta(days=6)

        showings = Showing.objects.filter(
            date__gte=today, date__lte=last_day).order_by(
            'date', 'start_hour', 'start_minutes')

        return showings
