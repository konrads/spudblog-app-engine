'use strict';

var user_name = 'john';

describe('module', function() {
  var RemoteResources;
  var $httpBackend;
  var $rootScope;
  var headerCtrl;

  // setup
  beforeEach(module('blogsApp'));
  beforeEach(inject(function (_$httpBackend_, _$rootScope_, $controller, _RemoteResources_) {
    RemoteResources = _RemoteResources_;
    $httpBackend = _$httpBackend_;
    $rootScope = _$rootScope_.$new();
    headerCtrl = $controller('HeaderCtrl', {$rootScope: $rootScope});

    // backend definition common for all tests
    $httpBackend.when('GET', '/api/full-blog/b0').respond({'result': 'ok'});
    $httpBackend.when('POST', '/api/blog').respond({'result': 'ok'});
  }));

  // teardown
  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });


  // Services tests
  describe('Get full blog (with posts)', function() {
    it('should GET /api/full-blog/<blog_id>', function() {
      $httpBackend.expectGET('/api/full-blog/b0');
      RemoteResources.getFullBlog('b0');
      $httpBackend.flush();
    });
  });

  describe('Create blog', function() {
    it('should POST /api/blog', function() {
      $httpBackend.expectPOST('/api/blog');
      RemoteResources.createBlog({}, function() {});
      $httpBackend.flush();
    });
  });


  // Controllers tests
  describe('Populate user_name', function() {
    it('should populate $rootScope with user_name', function() {
      expect($rootScope.user_name).toEqual(user_name);
    });
  });
});