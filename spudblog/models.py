from django.db import models
from django.contrib.auth.models import User


BACKGROUND_CHOICES = (
    ('plain-green', 'plain-green'),
    ('plain-blue', 'plain-blue'),
    ('plain-yellow', 'plain-yellow'),
)


DATE_FORMAT = '%Y/%m/%d %H:%M:%S'


class Blog(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    background = models.CharField(max_length=50, choices=BACKGROUND_CHOICES, default='plain-yellow')
    date_created = models.DateTimeField(auto_now_add=True)

    def as_json(self, inc_posts=True):
        if inc_posts:
            posts = [p.as_json() for p in self.post_set.order_by('date_created')]
        else:
            posts = []
        return {
            'id': self.id,
            'title': self.title,
            'background': self.background,
            'posts': posts,
            'date_created': self.date_created.strftime(DATE_FORMAT)
        }

    def __unicode__(self):
        return self.title


class Post(models.Model):
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def as_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'date_created': self.date_created.strftime(DATE_FORMAT)
        }

    def __unicode__(self):
        return self.title
