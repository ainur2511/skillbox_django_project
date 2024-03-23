import profile

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from shopapp.views import HelloView
from .views import *



app_name = 'myauth'
urlpatterns = [
    path('login/',
         LoginView.as_view(
             template_name='myauth/login.html',
             redirect_authenticated_user=True
         ),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about-me/', AboutMeView.as_view(), name='about_me'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/<int:pk>/update', ProfileUpdateView.as_view(), name='update_profile'),
    path('users/', UsersView.as_view(), name='users'),
    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_orders'),
    path('user/<int:pk>', AboutUserView.as_view(), name='about_user'),
]