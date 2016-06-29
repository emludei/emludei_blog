from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('posts.urls', namespace='posts')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^accounts/', include('userprofiles.urls', namespace='profiles')),
]
