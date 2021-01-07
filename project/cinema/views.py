from django.views.generic import ListView

from .models import Showing


class ScheduleView(ListView):
    template_name = 'cinema/schedule.html'
    model = Showing
    context_object_name = 'showings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weekdays'] = Showing.Weekday.choices

        return context

    def get_queryset(self):
        showings = Showing.objects.all().order_by('week_day_numerical', 'start_hour', 'start_minutes')

        return showings
