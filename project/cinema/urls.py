from django.urls import path

from .views import ScheduleView, MovieDetailView

urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie-detail-view'),
]
