from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('artilce/' , views.article, name='article'),
    path('about-us/' , views.aboutus, name='about_us'),
]
