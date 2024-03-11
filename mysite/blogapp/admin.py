from django.contrib import admin
from .models import *

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Author)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'content', 'author', 'category')

