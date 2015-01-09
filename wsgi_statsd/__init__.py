# -*- coding: utf-8 -*-
"""StatsdTimingMiddleware object."""
import time

__author__ = 'Wouter Lansu'
__version__ = '1.0.0'


class StatsdTimingMiddleware(object):

    """The Statsd timing middleware."""

    def __init__(self, app, client):
        """Initialize the middleware with an application and a Statsd client.

        :param app: The application object.
        :param client: `statsd.StatsClient` object.
        """
        self.app = app
        self.statsd_client = client

    def __call__(self, environ, start_response):
        """Call the application and time it.

        :param environ: Dictionary object, containing CGI-style environment variables.
        :param start_response: Callable used to begin the HTTP response.
        """
        interception = {}

        def start_response_wrapper(status, response_headers, exc_info=None):
            """Closure function to wrap the start_response in order to retrieve the status code which we need to
            generate the key name."""
            interception['status'] = status
            return start_response(status, response_headers, exc_info)

        # Time the call.
        start = time.time()
        result = self.app(environ, start_response_wrapper)
        stop = time.time()

        # Now we can generate the key name.
        key_name = '.'.join([environ['PATH_INFO'], environ['REQUEST_METHOD'], interception['status']])

        # Create the timer object and send the data to statsd.
        timer = self.statsd_client.timer(key_name)
        timer._start = start
        timer._stop = stop
        timer.stop()

        return result
