from django.urls import path

from .views import ScheduleView, MovieDetailView, ShowingDetailView

urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie-detail-view'),
    path('showing/<uuid:pk>/', ShowingDetailView.as_view(), name='showing-detail-view'),
]
