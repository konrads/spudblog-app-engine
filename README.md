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

You might need to tweak karma, I had to link the `karma` executable and setup `CHROME_BIN`:
```bash
ln node_modules/karma/bin/karma karma
export CHROME_BIN=/Applications/MyApps/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
```

Architecture
------------

This is a 'single page' application, driven by ajax requests.  UI is decoupled from the server side
and is responsible for its own rendering.  Django's contributions consist of:

* Login page - utilizing `django.contrib.admin`
* model data population for angularjs

The aim was to achieve uniformity of rendering, as opposed to common approach of partially rendering
in Django templates, partially via javascript.


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

The app has been deployed to Appspot [here](http://spudblog-ks.appspot.com/)


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
