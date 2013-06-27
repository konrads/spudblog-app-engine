"""Urls mappings for both UI views and REST api calls."""

from django.conf.urls import patterns, url
import django.contrib.auth.views

from spudblog import views

urlpatterns = patterns('',
    # UI view urls
    url(r'^$', django.contrib.auth.views.login,
            {'template_name': 'spudblog/login.html'}, name='login'),
    url(r'^blog-explorer/$', views.blog_explorer),
    url(r'^my-blogs/$', views.my_blogs),
    url(r'^logout/$', views.logout),

    # API urls
    url(r'^api/all/$', views.all),
    # Allow for optional /blog_id or /post_id - necessary for angularjs resource
    url(r'^api/full-blog(/(?P<blog_id>\d+))?$', views.full_blog),
    url(r'^api/blog(/(?P<blog_id>\d*))?$', views.blog),
    url(r'^api/post(/(?P<post_id>\d*))?$', views.post),
)