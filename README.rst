Hovercrafty
===========

Extensible Application DSL for Hoverfly, WSGI and any other backend

.. image:: https://readthedocs.org/projects/hovercrafty/badge/?version=latest
   :target: http://hovercrafty.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://travis-ci.org/newstore/hovercrafty.svg?branch=master
    :target: https://travis-ci.org/newstore/hovercrafty
.. |PyPI python versions| image:: https://img.shields.io/pypi/pyversions/hovercrafty.svg
   :target: https://pypi.python.org/pypi/hovercrafty
.. |Join the chat at https://gitter.im/newstore/hovercrafty| image:: https://badges.gitter.im/newstore/hovercrafty.svg
   :target: https://gitter.im/newstore/hovercrafty?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


Motivation
----------

Hovercrafty is a python library that leverages a single API to define
http request handlers, then run them as a hoverfly middleware, flask
application or WSGI container.


It was designed by NewStore Inc. to increase productivity of
developers who need to create and painlessly manage multiple hoverfly
mock servers that can react dinamically to different data input.  of
logic.




Install
-------

.. code:: bash

   pip install hovercrafty


Documentation
-------------

`:strike:hovercrafty.readthedocs.io <https://hovercrafty.readthedocs.io/en/latest/>`_


Basic Usage
-----------


Define Routes
^^^^^^^^^^^^^

**notice the intentional similarity with the Flask Application API interface**

.. code:: python

   import json

   from collections import OrderedDict
   from hovercrafty import RouteServer

   time_jsontest = RouteServer('time.jsontest.com', protocols=['http'])


   @time_jsontest.route('/')
   def index_time_json(request):
       data = OrderedDict([
           ("time", "02:44:49 AM"),
           ("milliseconds_since_epoch", 1519094689265),
           ("date", "02-20-2018"),
       ])
       return json.dumps(data)



With Hoverfly
^^^^^^^^^^^^^


Middleware
~~~~~~~~~~

Compatible with [hoverfly middleware]()

.. code:: python


   import json

   from collections import OrderedDict
   from hovercrafty.backends.hoverfly import HoverflyBackend
   from hovercrafty.codecs import JSONStreamCodec, UnicodeStreamCodec
   from hovercrafty import RouteServer

   time_jsontest = RouteServer('time.jsontest.com', protocols=['http'])


   @time_jsontest.route('/')
   def index_time_json(request):
       data = OrderedDict([
           ("time", "02:44:49 AM"),
           ("milliseconds_since_epoch", 1519094689265),
           ("date", "02-20-2018"),
       ])
       return json.dumps(data)


    # in the body of your `middleware.py`
    HoverflyBackend(time_jsontest).middleware(
        source=sys.stdin,
        destination=sys.stdout,
        codecs=[JSONStreamCodec]
    )


With Flask
^^^^^^^^^^

**Hovercrafty offers a few options:**


1. Create a fresh Flask app from a RouteServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from hovercrafty.backends.wsgi import FlaskBackend

   backend = FlaskBackend(time_jsontest)
   app = backend.create_application(__name__)
   app.run(port=8500)


2. Add routes to an existing Flask app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python


   from flask import Flask
   from hovercrafty.backends.wsgi import FlaskBackend
   from hovercrafty import RouteServer

   time_jsontest = RouteServer('http://time.jsontest.com')


   @time_jsontest.route('/')
   def index_time_json(request):
       data = OrderedDict([
           ("time", "02:44:49 AM"),
           ("milliseconds_since_epoch", 1519094689265),
           ("date", "02-20-2018"),
       ])
       return json.dumps(data)


   @time_jsontest.route('/')
   def index_time_json(request):
       data = OrderedDict([
           ("time", "02:44:49 AM"),
           ("milliseconds_since_epoch", 1519094689265),
           ("date", "02-20-2018"),
       ])
       return json.dumps(data)


   backend = FlaskBackend(time_jsontest)
   app = Flask(__name__)



   backend.register_routes_into(app)

   app.run(port=8500)




3. Process request from within a Flask handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   import json
   import sys

   from collections import OrderedDict

   from flask import Flask
   from flask import request

   from hovercrafty import RouteServer
   from hovercrafty.backends.wsgi import FlaskBackend

   httpbin_org = RouteServer('https://httpbin.org')
   time_jsontest = RouteServer('http://time.jsontest.com')

   @time_jsontest.route('/')
   def index_time_json(request):
       data = OrderedDict([
           ("time", "02:44:49 AM"),
           ("milliseconds_since_epoch", 1519094689265),
           ("date", "02-20-2018"),
       ])
       return json.dumps(data)


   backend = FlaskBackend(time_jsontest)
   app = Flask(__name__)


   @app.route('/httpbin/<path:path>')
   def namespace_httpbin_org(path):
       return backend.process_from_handler(request)

   app.run(port=8500)


As WSGI Container
^^^^^^^^^^^^^^^^^

**Compatible with any WSGI-compatible application container (e.g.: werkzeug, Django, ...)**

.. code:: python

   import json
   from werkzeug.wrappers import Request, Response
   from hovercrafty.backends.wsgi import WSGIBackend


   backend = WSGIBackend(time_jsontest)

   def application(environ, start_response):
       start_response('200 OK', [('Content-Type', 'application/json')])
       return [json.dumps({'hello': 'world'})]


   if __name__ == '__main__':
       from werkzeug.serving import run_simple
       run_simple('localhost', 8500, backend.handle_wsgi(application))
