# -*- coding: utf-8 -*-
""""""
import statsd

__author__ = 'Wouter Lansu'
__version__ = '0.1a1.dev1'


class StatsdTimingMiddleware(object):

    """The Statsd timing middleware."""

    def __init__(self, app, prefix, host, port):
        """If host or port are not defined a connection to Statsd cannot be made.

        :arg app: The application.
        :arg prefix: Helps distinguish multiple applications or environments using the same statsd server.
        :type prefix: str
        :arg host: The host running the statsd server, supports any kind of name or IP address.
        :type host: str
        :arg port: Statsd server port.
        :type port: str
        """
        self.app = app
        self.statsd_client = statsd.StatsClient(host, port, prefix)

    def __call__(self, environ, start_response):
        """Call the application and time it."""
        timer = self.statsd_client.timer(environ['PATH_INFO'])

        timer.start()
        application = self.app(environ, start_response)
        timer.stop()

        return application
