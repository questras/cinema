from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Order
from .forms import CreateOrderForm
from cinema.models import Showing


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = CreateOrderForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('schedule')  # todo: change to profile

    def get_showing(self):
        showing_uuid = self.kwargs['showing_uuid'] or None
        showing = get_object_or_404(Showing, pk=showing_uuid)
        return showing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['showing'] = self.get_showing()

        return context

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.showing = self.get_showing()

        if form.instance.tickets_amount > form.instance.showing.free_places():
            form.add_error(field='tickets_amount', error='Not enough available tickets.')
            return super().form_invalid(form)

        return super().form_valid(form)
