from django.urls import path
from . import views

urlpatterns = [
    path('houses/', views.house_list, name='house_list'),
    path('houses/<int:pk>/', views.HouseDetailView.as_view(), name='house_detail'),
    path('houses/new/', views.house_create, name='house_create'),
    path('houses/<int:pk>/edit/', views.HouseUpdateView.as_view(), name='house_update'),
    path('houses/<int:pk>/delete/', views.HouseDeleteView.as_view(), name='house_delete'),
    path('search/', views.search, name='search'),
] 