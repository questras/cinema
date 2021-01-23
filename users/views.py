from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import CustomUserCreationForm
from orders.models import Order


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'auth/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Replace hour and minute to 0 to include all tickets for current day.
        now = timezone.now().replace(hour=0, minute=0)
        tickets_history = self.request.user.my_orders.filter(showing__when__lt=now).order_by('showing__when')
        tickets_current = self.request.user.my_orders.filter(showing__when__gte=now).order_by('showing__when')
        tickets_for_cashier = None

        if self.request.user.is_cashier:
            tickets_for_cashier = Order.objects.filter(cashier_who_accepted__isnull=True,
                                                       showing__when__gte=now).order_by('showing__when')

        context['tickets_history'] = tickets_history
        context['tickets_current'] = tickets_current
        context['tickets_for_cashier'] = tickets_for_cashier

        return context


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('login')
    success_message = 'You registered successfully!'
