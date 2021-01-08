from django.urls import path

from .views import CreateOrderView

urlpatterns = [
    path('order/<uuid:showing_uuid>/', CreateOrderView.as_view(), name='create-order'),
]