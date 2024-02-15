from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *



app_name = 'myauth'
urlpatterns = [
    path('login/',
         LoginView.as_view(
             template_name='myauth/login.html',
             redirect_authenticated_user=True
         ),
         name='login'),
    path('cookie/get', get_cookie, name='get_cookie'),
    path('cookie/set', set_cookie, name='set_cookie'),
    path('session/get', get_session, name='get_session'),
    path('session/set', set_session, name='set_session'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about-me/', AboutMeView.as_view(), name='about_me'),
    path('register/', RegisterView.as_view(), name='register')

]