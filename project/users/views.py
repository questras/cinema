from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import CustomUserCreationForm
from orders.models import Order


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'auth/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        tickets_history = self.request.user.my_orders.filter(showing__when__lt=now)
        tickets_current = self.request.user.my_orders.filter(showing__when__gte=now)
        tickets_for_cashier = None

        if self.request.user.is_cashier:
            tickets_for_cashier = Order.objects.filter(cashier_who_accepted__isnull=True,
                                                       showing__when__gte=now)

        context['tickets_history'] = tickets_history
        context['tickets_current'] = tickets_current
        context['tickets_for_cashier'] = tickets_for_cashier

        return context


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('login')
