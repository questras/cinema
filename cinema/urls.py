from django.urls import path

from .views import (
    ScheduleView,
    MovieDetailView,
    ShowingDetailView,
    MovieListView,
    ShowingListView,
)

urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('showings/', ShowingListView.as_view(), name='showing-list'),
    path('showing/<uuid:pk>/', ShowingDetailView.as_view(), name='showing-detail-view'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie-detail-view'),
]
