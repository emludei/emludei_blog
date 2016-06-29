from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Post


class PostAdmin(SummernoteModelAdmin):
    fields = ['title', 'tags', 'body']
    list_display = ('title', 'pub_date')


admin.site.register(Post, PostAdmin)
