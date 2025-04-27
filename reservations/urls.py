from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('order/<int:pk>/', views.order_car, name='order_car'),
    path('create/<int:car_id>/', views.create_reservation, name='create_reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('renter-reservations/', views.renter_reservations, name='renter_reservations'),
    path('confirm/<int:reservation_id>/', views.confirm_reservation, name='confirm_reservation'),
    path('reject/<int:reservation_id>/', views.reject_reservation, name='reject_reservation'),
]

