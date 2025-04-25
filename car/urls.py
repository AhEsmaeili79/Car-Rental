from django.urls import path
from . import views

urlpatterns = [
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/new/', views.car_create, name='car_create'),
    path('cars/<int:pk>/edit/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
    path('search/', views.search, name='search'),
] 