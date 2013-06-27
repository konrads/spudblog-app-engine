'use strict';

/* App specific */

angular.module('blogsApp', ['spudServices'])
    .config(function($interpolateProvider, $routeProvider, $httpProvider) { 
        $interpolateProvider.startSymbol('[['); 
        $interpolateProvider.endSymbol(']]');
        $routeProvider.when('/blog-view/:id', { controller: 'BlogViewCtrl', templateUrl: "blog-view.tpl.html" });
        $routeProvider.when('/blog-edit/:id', { controller: 'BlogEditCtrl', templateUrl: "blog-edit.tpl.html" });
        // handle ajax unautherized calls
        var interceptor = ['$rootScope', '$q', function (scope, $q) {
            function success(response) {
                return response;
            }

            function error(response) {
                alert('Error: ' + response.data.substring(0, 1000) + '\nReloading...');
                location.replace('');
            }

            return function (promise) {
                return promise.then(success, error);
            }
        }];
        $httpProvider.responseInterceptors.push(interceptor);
    })
    .controller('HeaderCtrl', function ($rootScope) {
        if (typeof(user_name) != 'undefined') $rootScope.user_name = user_name;
    })
    .controller('BlogSummariesCtrl', function ($scope, $location, RemoteResources) {
        $scope.blog_summaries = blog_summaries;
        
        $scope.isActive = function(route) {
            return route === $location.path();
        };
        $scope.newBlog = function() {
            // hack to create an empty blog, as blog_id is used for url
            var new_blog = {title: 'New Blog', content: '', background: $scope.backgrounds[0].class};
            RemoteResources.createBlog(new_blog, function(blog) {
                blog['posts'] = [];
                $scope.blog_summaries.push(blog);
                $location.path('/blog-edit/' + blog.id);
            });
        };
        // on deleted blog - redirect to home
        $scope.$on('DELETE_BLOG', function(event, blog_id) {
            for (var i=0; i<$scope.blog_summaries.length; i++) {
                if ($scope.blog_summaries[i].id === blog_id) {
                    $scope.blog_summaries.splice(i, 1);
                    break;
                }
            }
            $location.path('');
        });
        // on blog rename
        $scope.$on('UPDATE_BLOG', function(event, blog) {
            var blog_summ = _.findWhere($scope.blog_summaries, {id: blog.id});
            blog_summ.title = blog.title;
        });
    })
    .controller('BlogViewCtrl', function ($scope, $routeParams, RemoteResources) {
        if ($routeParams.id) $scope.blog = RemoteResources.getFullBlog($routeParams.id);
    })
    .controller('BlogEditCtrl', function ($scope, $rootScope, $routeParams, RemoteResources) {
        $rootScope.backgrounds = [
            {name: 'green', class: 'plain-green'},
            {name: 'blue', class: 'plain-blue'},
            {name: 'yellow', class: 'plain-yellow'},
        ];
        if ($routeParams.id) $scope.blog = RemoteResources.getFullBlog($routeParams.id);

        // fsm for editing/saving, including the action names, states
        $scope.blogState = new BlogState(RemoteResources, $scope.blog);
        // FIXME: should use $watches on the blogState's model and state
    });
