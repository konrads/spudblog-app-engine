Spudblog app
============

A simple blogging application that serves as a playground for technologies:

* Django ( [djangoappengine](https://github.com/django-nonrel/djangoappengine) variety )
* Google App Engine (persisting via Datastore)
* Angularjs
* Bootstrap
* Jasmine/Karma for JS testing


Dev environment
---------------

Run build.sh which should fetch djangoappengine and dependants.

For testing, I've used the mock library:
```bash
pip install mock
```

For Javascript testing, I've installed karma and jasmine-node via npm:

```javascript
npm install karma jasmine-node
```

Karma install might need tweaking, I had to link the `karma` executable and setup `CHROME_BIN`:
```bash
ln -s node_modules/karma/bin/karma karma
export CHROME_BIN=/Applications/MyApps/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
```

Architecture
------------

This is a 3 tier application consisting of:

* Angularjs front end
* Django backend serving REST request to Angularjs
* Google app engine deployment, utilizing Datastore persistence

The UI is a 'single page' application, driven by ajax REST requests.  It is decoupled from the server side
and hence, responsible for its own rendering.  Django's contribution consist of:

* Login page - utilizing `django.contrib.admin`
* model data population for angularjs (but not rendering)

The aim was to achieve uniformity of rendering (via javascript), as opposed to common approach of partially rendering
in Django templates, partially via javascript.

Django serves up prepopulated html pages:

* / - login page
* /blog-explorer - unauthenticated read only list of all blogs
* /my-blogs - authenticated list of user's blogs/posts

Additionally, there's REST api:
* /api/all - GETs all users, their blogs and posts
* /api/full-blog/<blog_id> - GETs blog and its posts
* /api/blog/<blog_id> - POSTs/PUTs/DELETEs blog.  Requires authentication (session cookie).  For POST, /<blog_id> is not required
* /api/post/<post_id> - POSTs/PUTs/DELETEs post.  Requires authentication (session cookie).  For POST, /<post_id> is not required

For persistence, Datastore is mapped via models of [djangoappengine](https://github.com/django-nonrel/djangoappengine).  This mapping
is Django friendly and works within /admin interface.


To run
------

First create a superuser:
```bash
python manage.py createsuperuser
```
Startup the server:
```bash
python manage.py runserver
# or to clear the datastore:
python manage.py runserver -c
```

Login to [http://127.0.0.1:8000/admin/] and prepulate Users/Blogs/Posts.
Browse existing logs via: [http://127.0.0.1:8000/blog-explorer] or go login and edit actual app: [http://127.0.0.1:8000/].

For remote deployement (eg. `appspot`), first create app in the appspot, then:
```bash
python manage.py deploy
python manage.py remote createsuperuser
```

The app has been deployed to Appspot [here](http://spudblog-ks.appspot.com/).


Testing
-------

2 types of tests has been created, Python and Javascript.  To run Python ones:
```python
python manage.py test spudblog -v 2
```

To run Javascript ones:
```javascript
karma start js-tests/config/karma.conf.js $*
```


Snags
-----

Angularjs interactions are not safe from csfr attacks the way Django templates can be via csfr_token.
Due to the dynamic nature of ajax, such token could be either supplied once per session, or piggybacked
onto every response.

Ajax error handling is simplistic, prompting an alert box with the error message, followed by the
reload of the `my-blogs` page - this could result with issues if the `my-blogs` page has errors.

Django lacks support for REST PATCH, which suits this app better than PUT.
[django-rest-framework](http://django-rest-framework.org/) could be of help here,
however it's been discounted to minimize the bloat of App Engine unsupported libraries.

REST versioning was abandoned, possible approach described [here](http://blog.steveklabnik.com/posts/2011-07-03-nobody-understands-rest-or-http#i_want_my_api_to_be_versioned).  This would involve setting content-type to "application/vnd.spudblog-v1+json"
in both Django views and Angularjs's REST mechanism.