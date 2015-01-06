wsgi_statsd documentation
=========================

wsgi_statsd is a WSGI middleware that you can use to wrap your existing wsgi application.
It provides an easy way to time all requests.

Usage
-----

In your wsgi.py file wrap your WSGI application as follows:

.. code-block:: python

   import StatsdTimingMiddleware

   application = StatsdTimingMiddleware(original_application, 'statsd_prefix', 'statsd_host', 8125)

What it does
------------

The middleware uses the statsd timer function, using the environ['PATH_INFO'] variable as a namespace.
It sends the amount of time the request took to the statsd server.

That's it.

If you want more granular reporting you'll have to work with the `prefix` argument. You can pass any string you want
and the middleware will pass it along to statsd.

Using the `foo` prefix and calling the `www.spam.com/bar` page will result in `foo.bar` having a value equal to the
time it took to handle the request.
