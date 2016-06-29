from django.conf.urls import url

from comments import views as comment_views

from . import views
from .models import Post


urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^posts/tag/(?P<slug>\w+)/$', views.TaggedPosts.as_view(), name='objects_for_tag'),

    url(r'^addcomment/$', comment_views.AddComment.as_view(), {'model': Post}, name='add_comment'),
    url(r'^removecomment/$', comment_views.RemoveComment.as_view(), name='remove_comment'),
    url(r'^removecomment_tree/$', comment_views.RemoveCommentTree.as_view(), name='remove_comment_tree'),
]
