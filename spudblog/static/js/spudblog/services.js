'use strict';

/* Services */
function BlogState(RemoteResources, blog) {
    var currModel = blog;
    var parentBlog = blog;
    var state = 'saved';

    this.doBlogAction = function(blog) {
        currModel = blog;
        if (state === 'editing') {
            // FIXME: saving object with no posts
            RemoteResources.updateBlog(blog);
        }

        state = (state === 'editing') ? 'saved' : 'editing';
    };

    this.doPostAction = function(post) {
        currModel = post;
        if (state === 'editing') {
            if (post.id) {
                RemoteResources.updatePost(post);
            } else {
                RemoteResources.createPost(post, parentBlog);
            }
        }

        state = (state === 'editing') ? 'saved' : 'editing';
    };

    this.actionName = function(model) {
        var actionName;
        if (currModel.id === model.id && state === 'editing')
            actionName = 'Save';
        else
            actionName = "Edit";
        return actionName;
    };

    this.editingDisabled = function(model) {
        var enabled = (currModel.id === model.id && state === 'editing');
        return ! enabled;
    };

    this.actionDisabled = function(model) {
        var enabled = (currModel.id === model.id || state === 'saved');
        return ! enabled;
    };

    this.addNewDisabled = function() {
        return state === 'editing';
    };

    this.addPost = function() {
        var post = { title: null, content: null };
        blog.posts.push(post);
        currModel = post;
        state = 'editing';
    };

    this.deletePost = function(post) {
        RemoteResources.deletePost(post, parentBlog);
        state = 'saved';
    };

    this.deleteBlog = function(blog) {
        RemoteResources.deleteBlog(blog);  
    };
};

angular.module('spudServices', ['ngResource']).
    factory('RemoteResources', function($resource, $rootScope) {
        var RemoteResources = function() {
            var fullBlogRes = $resource('/api/full-blog/:id', {id: '@id'});
            var blogRes = $resource('/api/blog/:id', {id: '@id'}, {update: {method:'PUT'}});
            var postRes = $resource('/api/post/:id', {id: '@id'}, {update: {method:'PUT'}});

            var updateCallback = function(org) {
                return function(updated) {
                    for(var key in updated)
                        org[key] = updated[key];
                };
            };
            var deleteCallback = function(deleted, collection) {
                // check by id, in case we're dealing with blogs/blogSummaries
                return function() {
                    var ind = collection.indexOf(deleted);
                    collection.splice(ind, 1);
                };
            };
            var deleteBlogCallback = function(blog) {
                $rootScope.$broadcast('DELETE_BLOG', blog.id);
            };
            var updateBlogCallback = function(blog) {
                $rootScope.$broadcast('UPDATE_BLOG', blog);
            };

            // public API
            this.getFullBlog = function(id) {
                return fullBlogRes.get({id: id});
            };
            this.createBlog = function(blog, createBlogCallback) {
                var b = angular.copy(blog);
                delete b.blogs;
                return blogRes.save(b, createBlogCallback);
            };
            this.updateBlog = function(blog) {
                var b = angular.copy(blog);
                delete b.posts;
                return blogRes.update(b, updateBlogCallback);
            };
            this.deleteBlog = function(blog) {
                return blogRes.delete({id: blog.id}, deleteBlogCallback);
            };
            this.createPost = function(post, blog, successFun) {
                var p = angular.extend(post, {blog_id: blog.id});
                return postRes.save(p, updateCallback(post));
            };
            this.updatePost = function(post) {
                return postRes.update(post, updateCallback(post));
            };
            this.deletePost = function(post, parentBlog) {
                if (post.id)
                    return postRes.delete({id: post.id}, deleteCallback(post, parentBlog.posts));
                else
                    deleteCallback(post, parentBlog.posts)();
            };
        };
        return new RemoteResources();
    });
