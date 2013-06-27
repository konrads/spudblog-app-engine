"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import json
from django.test import TestCase
from mock import Mock
from django.test.client import Client
from django.http import HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.models import User
import spudblog.views as views
from spudblog.models import Blog, Post


def _request(http_method, needs_login):
    class User(object):
        is_authenticated = Mock(return_value=needs_login)
    class Request(object):
        user = User()
        method = http_method
    return Request()

@views.api_call()
def get_no_login(request):
    return { 'a': 1 }

@views.api_call(needs_login=True)
def get_need_login(request):
    return { 'a': 1 }

@views.api_call(methods=['POST'])
def post_no_login(request):
    return { 'a': 1 }


class ApiCallDecoratorTest(TestCase):
    def test_get_no_login(self):
        req = _request('GET', True)
        self.assertIs(type(get_no_login(req)), HttpResponse)
        self.assertFalse(req.user.is_authenticated.called)

        req = _request('GET', False)
        self.assertIs(type(get_no_login(req)), HttpResponse)
        self.assertFalse(req.user.is_authenticated.called)

    def test_get_need_login(self):
        req = _request('GET', True)
        self.assertIs(type(get_need_login(req)), HttpResponse)
        self.assertTrue(req.user.is_authenticated.called)

        req = _request('GET', False)
        self.assertIs(type(get_need_login(req)), HttpResponseForbidden)
        self.assertTrue(req.user.is_authenticated.called)

    def test_post_no_login(self):
        req = _request('POST', False)
        self.assertIs(type(post_no_login(req)), HttpResponse)
        self.assertFalse(req.user.is_authenticated.called)

        req = _request('GET', False)
        self.assertIs(type(post_no_login(req)), HttpResponseNotAllowed)
        self.assertFalse(req.user.is_authenticated.called)


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='john')
        self.user.set_password('pass')
        self.blog1 = Blog.objects.create(author=self.user, title='Writing spudblog', background='plain-green')
        self.post1_1 = Post.objects.create(blog=self.blog1, title='Angularjs UI', content='Creating models and views')
        self.post1_2 = Post.objects.create(blog=self.blog1, title='Django server', content='Creating site and app')
        self.blog2 = Blog.objects.create(author=self.user, title='Deploying spudblog', background='plain-blue')
        self.user.save()


class ApiTest(BaseTestCase):
    """Tests for api calls."""

    def test_get_full_blog(self):
        response = self.client.get('/api/full-blog/%d' % self.blog1.id)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)

        # Check that the rendered context contains 5 customers.
        self.assertEquals(content['title'], 'Writing spudblog')
        self.assertEquals(2, len(content['posts']))
        self.assertEquals('Creating models and views', content['posts'][0]['content'])
        self.assertEquals('Creating site and app', content['posts'][1]['content'])

    def test_blog_create(self):
        self.client.login(username='john', password='pass')
        new_blog = {'title': 'Delivering spudblog', 'background': 'plain-blue'}
        response = self.client.post('/api/blog/', content_type='application/json', data=json.dumps(new_blog))
        self.assertEquals(response.status_code, 200)
        created_blog = json.loads(response.content)
        self.assertIsNotNone(created_blog['id'])  # new id!
        self.assertEquals(new_blog['title'], created_blog['title'])

    def test_blog_udate(self):
        self.client.login(username='john', password='pass')
        changed_blog = {'title': 'Delivering spudblog'}
        response = self.client.put('/api/blog/%d' % self.blog2.id, content_type='application/json', data=json.dumps(changed_blog))
        self.assertEquals(response.status_code, 200)
        updated_blog = json.loads(response.content)
        self.assertEquals(self.blog2.id, updated_blog['id'])  # unaltered
        self.assertEquals(changed_blog['title'], updated_blog['title'])
        self.assertEquals('plain-blue', updated_blog['background'])  # un-altered


class UIViewTest(BaseTestCase):
    """Tests for UI views."""
    def test_my_blogs(self):
        self.client.login(username='john', password='pass')
        response = self.client.get('/my-blogs/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals('Writing spudblog', response.context.get('blogs')[0].title)
        self.assertEquals('Deploying spudblog', response.context.get('blogs')[1].title)

