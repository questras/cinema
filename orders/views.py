from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied

from .models import Order
from .forms import CreateOrderForm
from cinema.models import Showing


def finalize_order(request, order_uuid, accepted):
    if not request.user.is_cashier:
        raise PermissionDenied

    order = get_object_or_404(Order, pk=order_uuid)

    if not order.cashier_who_accepted:
        order.cashier_who_accepted = request.user
        order.accepted = accepted
        order.save()
        messages.success(request, 'Order has been finalized successfully.')

    return redirect('profile')


@login_required()
def accept_order_view(request, order_uuid):
    return finalize_order(request, order_uuid, True)


@login_required()
def reject_order_view(request, order_uuid):
    return finalize_order(request, order_uuid, False)


class CreateOrderView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Order
    form_class = CreateOrderForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('profile')
    success_message = 'Tickets booked successfully!'

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
