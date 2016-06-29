from django.views.generic import ListView, DetailView
from django.contrib.contenttypes.models import ContentType

from taggit.models import TaggedItem

from .models import Post


class TaggedPosts(ListView):
    template_name = 'posts/list_posts.html'
    context_object_name = 'posts'
    model = Post
    paginate_by = 20

    def get_queryset(self):
        ids = TaggedItem.objects.filter(
            tag__slug=self.kwargs['slug'],
            content_type=ContentType.objects.get_for_model(self.model)
        ).values_list('object_id', flat=True)

        return self.model.objects.filter(pk__in=ids)


class PostListView(ListView):
    model = Post
    template_name = 'posts/list_posts.html'
    context_object_name = 'posts'
    paginate_by = 20


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

