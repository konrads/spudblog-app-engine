"""Views, both for UI presentation and for api calls.

UI views have no prefix, api calls are prefixed with 'api'
"""

from functools import wraps
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import login as django_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import db


def api_call(methods=None, needs_login=False):
    """Enforces valid http method has been used, if `needs_login`
    - validates the user is authenticated, converts KeyError into Http404.

    :param methods: valid http methods ('GET', 'POST', 'PUT', 'DELETE')
    :param needs_login: if authenticated user session needs to be present
    :returns: decorated view
    """
    if not methods:
        methods = ['GET']

    def decorator(f):
        @wraps(f)
        def wrapper(request, *args, **kwds):
            if needs_login and not request.user.is_authenticated():
                return HttpResponseForbidden('Unauthorized/timed out user')
            if request.method not in methods:
                return HttpResponseNotAllowed(methods)
            res = None
            try:
                res = f(request, *args, **kwds)
            except KeyError:
                pass
            if not res:
                return HttpResponseNotFound('Resource not found')
            return HttpResponse(json.dumps(res, indent=4), mimetype='application/json')
        # do not need csfr for REST api...?
        return csrf_exempt(wrapper)
    return decorator


##### html views
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')


def blog_explorer(request):
    return render(request, 'spudblog/blog_explorer.html', {'blogs': db.get_blogs()})


@login_required
def my_blogs(request):
    return render(
        request,
        'spudblog/my_blogs.html',
        {'blogs': db.get_blogs(request.user.id), 'user_name': request.user.username})


##### API
@api_call()
def all(request):
    """Debug api call, lists all users, their blogs and posts."""
    return db.all_as_json()


@api_call()
def full_blog(request, blog_id):
    """Gets full blog, with title, id, posts."""
    blog_id = long(blog_id)
    return db.get_full_blog(blog_id).as_json()


@api_call(methods=['POST', 'PUT', 'DELETE'], needs_login=True)
def blog(request, blog_id):
    """CRUD operations on blog, ie. create, update and delete
    (no fetch, that's done within :func:`views.full-blog`)."""
    if request.method == 'POST':
        blog = json.loads(request.body)
        return db.create_blog(request.user.id, blog).as_json()
    elif request.method == 'PUT':
        blog_id = long(blog_id)
        blog = json.loads(request.body)
        blog['id'] = blog_id  # whether id's set or not...
        return db.update_blog(blog).as_json()
    elif request.method == 'DELETE':
        blog_id = long(blog_id)
        return db.del_blog(blog_id)


@api_call(methods=['POST', 'PUT', 'DELETE'], needs_login=True)
def post(request, post_id):
    """CRUD operations on post, ie. create, update and delete
    (no fetch, that's done within :func:`views.full-blog`."""
    if request.method == 'POST':
        post = json.loads(request.body)
        blog_id = post.pop('blog_id')
        return db.create_post(blog_id, post).as_json()
    elif request.method == 'PUT':
        post_id = long(post_id)
        post = json.loads(request.body)
        return db.update_post(post).as_json()
    elif request.method == 'DELETE':
        post_id = long(post_id)
        return db.del_post(post_id)
