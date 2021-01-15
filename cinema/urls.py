from django.urls import path

from .views import (
    ScheduleView,
    MovieDetailView,
    ShowingDetailView,
    MovieListView,
)

urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie-detail-view'),
    path('showing/<uuid:pk>/', ShowingDetailView.as_view(), name='showing-detail-view'),
]
