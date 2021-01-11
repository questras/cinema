from django.urls import path

from .views import CreateOrderView, accept_order_view, reject_order_view

urlpatterns = [
    path('order/<uuid:showing_uuid>/', CreateOrderView.as_view(), name='create-order'),
    path('order/<uuid:order_uuid>/accept/', accept_order_view, name='accept-order'),
    path('order/<uuid:order_uuid>/reject/', reject_order_view, name='reject-order'),
]
