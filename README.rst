Hovercrafty
=======

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



Install
-------

.. code:: bash

   pip install hovercrafty


Documentation
-------------

`hovercrafty.readthedocs.io <https://hovercrafty.readthedocs.io/en/latest/>`_


Basic Usage
-----------


Define Routes
^^^^^^^^^^^^^

**notice the intentional similarity with the Flask Application API interface**

.. code:: python

   import json
   import sys

   from collections import OrderedDict
   from hovercrafty import RouteServer

   time_jsontest_com = RouteServer('time.jsontest.com', protocols=['http'])


   @time_jsontest_com.route('/')
   def index_time_json(request):
       data = OrderedDict([
           ("time", "02:44:49 AM"),
           ("milliseconds_since_epoch", 1519094689265),
           ("date", "02-20-2018"),
       ])
       return json.dumps(data)



With Hoverfly
^^^^^^^^^^^^^

.. code:: python

    from hovercrafty.backends.hoverfly import HoverflyMiddleware
    from hovercrafty.codecs import JSONStreamCodec, UnicodeStreamCodec

    # in the body of your `middleware.py`
    HoverflyMiddleware(time_jsontest_com).run(
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
   time_jsontest_com = RouteServer('http://time.jsontest.com')


   backend = FlaskBackend(time_jsontest)
   app = Flask(__name__)


   @app.route('/httpbin/<path:path>')
   def namespace_httpbin_org(path):
       backend.process_from_handler()

   app.run(port=8500)
