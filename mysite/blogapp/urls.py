from django.urls import path
from blogapp.views import PostListView



urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts')
]