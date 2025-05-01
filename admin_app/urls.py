from django.urls import path
from . import views

urlpatterns = [
    # Admin Panel
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    
    # User Management
    path('admin_panel/users/', views.admin_users, name='admin_users'),
    
    # Order Management
    path('admin_panel/orders/', views.admin_orders, name='admin_orders'),
    
    # Car Management
    path('admin_panel/cars/', views.admin_cars, name='admin_cars'),
    
    # Renter-related Management
    path('admin_panel/renter_requests/', views.renter_requests, name='renter_requests'),
    path('renter-cars/', views.renter_cars, name='renter_cars'),
    
    # Action URLs
    path('admin_panel/toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('admin_panel/delete_user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('admin_panel/toggle_car_status/<int:car_id>/', views.toggle_car_status, name='toggle_car_status'),
    path('admin_panel/delete_car/<int:car_id>/', views.admin_delete_car, name='admin_delete_car'),
    path('admin_panel/delete_order/<int:order_id>/', views.admin_delete_order, name='admin_delete_order'),
    path('car_detail/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car_update/<int:pk>/', views.car_update, name='car_update'),
]
