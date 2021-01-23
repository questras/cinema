from django.urls import path

from .views import (
    StaffPanelView,
    CreateMovieView,
    DeleteMovieView,
    CreateHallView,
    DeleteHallView,
    CreateShowingView,
    DeleteShowingView,
    ManageCashiersView,
)

urlpatterns = [
    path('panel/', StaffPanelView.as_view(), name='staff-panel'),
    path('create-movie/', CreateMovieView.as_view(), name='create-movie'),
    path('delete-movie/<slug:slug>/', DeleteMovieView.as_view(), name='delete-movie'),
    path('create-hall/', CreateHallView.as_view(), name='create-hall'),
    path('delete-hall/<int:pk>/', DeleteHallView.as_view(), name='delete-hall'),
    path('create-showing/', CreateShowingView.as_view(), name='create-showing'),
    path('delete-showing/<uuid:pk>/', DeleteShowingView.as_view(), name='delete-showing'),
    path('manage_cashiers/', ManageCashiersView.as_view(), name='manage-cashiers'),
]
