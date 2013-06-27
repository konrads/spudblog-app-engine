from django.contrib import admin
from spudblog.models import Blog, Post


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class BlogAdmin(admin.ModelAdmin):
    inlines = [PostInline]


admin.site.register(Blog, BlogAdmin)
