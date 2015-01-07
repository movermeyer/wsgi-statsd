# -*- coding: utf-8 -*-
"""StatsdTimingMiddleware object."""

__author__ = 'Wouter Lansu'
__version__ = '1.0.0'


class StatsdTimingMiddleware(object):

    """The Statsd timing middleware."""

    def __init__(self, app, client):
        """Initialize the middleware with an application and a Statsd client.

        :arg app: The application.
        :arg client: `statsd.StatsClient` object.
        """
        self.app = app
        self.statsd_client = client

    def __call__(self, environ, start_response):
        """Call the application and time it."""
        key_name = environ['PATH_INFO'] + '.' + environ['REQUEST_METHOD']

        with self.statsd_client.timer(key_name):
            result = self.app(environ, start_response)

        return result
