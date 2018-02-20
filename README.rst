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


.. code:: python

    import json
    import sys

    from collections import OrderedDict
    from hovercrafty import RouteServer

    from hovercrafty.backends.hoverfly import HoverflyMiddleware
    from hovercrafty.codecs import JSONStreamCodec

    time_jsontest_com = RouteServer('time.jsontest.com', protocols=['http'])


    @time_jsontest_com.route('/')
    def index_time_json(request):
         data = OrderedDict([
           ("time", "02:44:49 AM"),
           ("milliseconds_since_epoch", 1519094689265),
           ("date", "02-20-2018"),
         ])
         return json.dumps(data)


     if __name__ == '__main__':
         HoverflyMiddleware(time_jsontest_com).run(
             source=sys.stdin,
             destination=sys.stdout,
             codecs=[JSONStreamCodec]
         )
