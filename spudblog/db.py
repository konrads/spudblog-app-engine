"""Persisntence abstraction.

Limits persistence interactions - all persisted data goes through this layer.
"""

from django.contrib.auth.models import User
from spudblog.models import Blog, Post


###### API
def get_blogs(user_id=None):
    if user_id:
        return Blog.objects.filter(author_id=user_id).order_by('date_created')
    else:
        return Blog.objects.order_by('date_created')


### Common API
def all_as_json():
    """Debug api call, return all users, their blogs and posts."""
    users = []
    for u in User.objects.order_by('username'):
        blogs = [b.as_json() for b in u.blog_set.order_by('date_created')]
        users.append({'id': u.id, 'username': u.username, 'blogs': blogs})
    return users


def get_full_blog(blog_id):
    """Gets full blog, with title, id, posts."""
    return Blog.objects.get(id=blog_id)


### Blog API
def create_blog(user_id, blog):
    new_blog = Blog(author_id=user_id,
                    title=blog['title'],
                    background=blog['background'])
    new_blog.save()
    return new_blog


def update_blog(blog):
    updated_blog = Blog.objects.get(id=blog['id'])
    if 'title' in blog:
        updated_blog.title = blog['title']
    if 'background' in blog:
        updated_blog.background = blog['background']
    updated_blog.save()
    return updated_blog


def del_blog(blog_id):
    deleted_blog = Blog.objects.get(id=blog_id)
    # need to delete posts manually
    for p in deleted_blog.post_set.all():
        p.delete()
    deleted_blog.delete()
    return {'id': blog_id}


### Post API
def create_post(blog_id, post):
    new_post = Post(blog_id=blog_id,
                    title=post['title'],
                    content=post['content'])
    new_post.save()
    return new_post


def update_post(post):
    updated_post = Post.objects.get(id=post['id'])
    if 'title' in post:
        updated_post.title = post['title']
    if 'content' in post:
        updated_post.content = post['content']
    updated_post.save()
    return updated_post


def del_post(post_id):
    deleted_post = Post.objects.get(id=post_id)
    deleted_post.delete()
    return {'id': post_id}
