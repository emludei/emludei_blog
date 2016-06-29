from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views

from . import views
from . import forms


urlpatterns = [
    url(r'^registration/$', views.Registration.as_view(), name='registration'),
    url(r'^activate/(?P<activation_key>\w+)/$', views.activate, name='activate'),
    url(r'^user/(?P<username>\w+)/$', views.profile_view, name='profile'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^password/change/$',
        auth_views.password_change,
        {
            'template_name': 'userprofiles/password_change.html',
            'password_change_form': forms.UserPasswordChangeForm,
            'post_change_redirect': reverse_lazy('profiles:password_change_done')
        },
        name='password_change'),

    url(r'^password/change/done/$',
        auth_views.password_change_done,
        {
            'template_name': 'userprofiles/password_change_done.html'
        },
        name='password_change_done'),

    url(r'^password/reset/$',
        auth_views.password_reset,
        {
            'template_name': 'userprofiles/password_reset.html',
            'email_template_name': 'userprofiles/password_reset_email.html',
            'subject_template_name': 'userprofiles/password_reset_email_subject.txt',
            'password_reset_form': forms.UserPasswordResetForm,
            'post_reset_redirect': reverse_lazy('profiles:password_reset_done'),
        },
        name='password_reset'),

    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {
            'template_name': 'userprofiles/password_reset_done.html',
        },
        name='password_reset_done'),

    url(r'^password/reset/confirm/(?P<uidb64>[0-9a-zA-Z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {
            'template_name': 'userprofiles/password_reset_confirm.html',
            'post_reset_redirect': reverse_lazy('profiles:password_reset_complite'),
            'set_password_form': forms.UserPasswordSetForm,
        },
        name='password_reset_confirm'),

    url(r'^password/reset/complite/$',
        auth_views.password_reset_complete,
        {
            'template_name': 'userprofiles/password_reset_complite.html',
        },
        name='password_reset_complite'),

    url(r'^thanks/$', views.thanks, name='thanks'),
]
