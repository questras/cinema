from django.views.generic import TemplateView, CreateView, DeleteView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import CreateShowingForm, SelectUserForm
from cinema.models import Showing, Movie, Hall
from django.contrib.auth import get_user_model

User = get_user_model()


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to assure that the user accessing the view is a staff member."""

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class StaffPanelView(StaffRequiredMixin, TemplateView):
    template_name = 'staff_panel/staff_panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['showings'] = Showing.objects.all()
        context['movies'] = Movie.objects.all()
        context['halls'] = Hall.objects.all()

        return context


class CreateMovieView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Movie
    template_name = 'staff_panel/create_movie.html'
    fields = ('title', 'director', 'year_of_production', 'type',
              'duration_in_minutes', 'description')
    success_message = 'Movie created!'
    success_url = reverse_lazy('staff-panel')


class DeleteMovieView(StaffRequiredMixin, DeleteView):
    model = Movie
    template_name = 'staff_panel/delete_movie.html'
    context_object_name = 'movie'
    success_message = 'Movie deleted!'
    success_url = reverse_lazy('staff-panel')

    def delete(self, request, *args, **kwargs):
        response = super(DeleteMovieView, self).delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response


class CreateShowingView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Showing
    form_class = CreateShowingForm
    template_name = 'staff_panel/create_showing.html'
    success_message = 'Showing created!'
    success_url = reverse_lazy('staff-panel')


class DeleteShowingView(StaffRequiredMixin, DeleteView):
    model = Showing
    template_name = 'staff_panel/delete_showing.html'
    context_object_name = 'showing'
    success_message = 'Showing deleted!'
    success_url = reverse_lazy('staff-panel')

    def delete(self, request, *args, **kwargs):
        response = super(DeleteShowingView, self).delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response


class CreateHallView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Hall
    template_name = 'staff_panel/create_hall.html'
    fields = ('places',)
    success_message = 'Hall created!'
    success_url = reverse_lazy('staff-panel')


class DeleteHallView(StaffRequiredMixin, DeleteView):
    model = Hall
    template_name = 'staff_panel/delete_hall.html'
    context_object_name = 'hall'
    success_message = 'Hall deleted!'
    success_url = reverse_lazy('staff-panel')

    def delete(self, request, *args, **kwargs):
        response = super(DeleteHallView, self).delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response


class ManageCashiersView(StaffRequiredMixin, FormView):
    form_class = SelectUserForm
    template_name = 'staff_panel/manage_cashiers.html'
    success_url = reverse_lazy('manage-cashiers')

    def get_context_data(self, **kwargs):
        context = super(ManageCashiersView, self).get_context_data(**kwargs)
        context['cashiers'] = User.objects.filter(is_cashier=True)
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email') or ''
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            if 'promote' in request.POST:
                user.is_cashier = True
                msg = 'promoted'
            elif 'demote' in request.POST:
                user.is_cashier = False
                msg = 'demoted'
            else:
                # Unknown post request.
                messages.error(request, 'Something went wrong!')
                return super(ManageCashiersView, self).post(request, *args, **kwargs)

            user.save()
            messages.success(request, f'{user.get_full_name()} ({user.email}) {msg}!')
        else:
            messages.error(request, f'User with email: {email} does not exist!')

        return super(ManageCashiersView, self).post(request, *args, **kwargs)
