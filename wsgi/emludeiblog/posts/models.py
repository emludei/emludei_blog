from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from django_summernote.widgets import SummernoteWidget

from taggit.managers import TaggableManager
from comments.models import Comment


class Post(models.Model):
    title = models.CharField(verbose_name='title', max_length=300)
    body = models.TextField()
    pub_date = models.DateTimeField(verbose_name='publication date', auto_now_add=True)

    tags = TaggableManager()
    comments = GenericRelation(Comment)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
