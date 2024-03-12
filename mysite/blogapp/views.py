from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Post


class PostListView(ListView):
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags').defer('content', 'author__bio')
    template_name = 'post_list.html'
    context_object_name = 'posts'
