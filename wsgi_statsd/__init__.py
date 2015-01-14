"""StatsdTimingMiddleware object."""
import time

__version__ = '0.2.1'


class StatsdTimingMiddleware(object):

    """The Statsd timing middleware."""

    def __init__(self, app, client, time_exceptions=False):
        """Initialize the middleware with an application and a Statsd client.

        :param app: The application object.
        :param client: `statsd.StatsClient` object.
        :param time_exceptions: send stats when exception happens or not, `False` by default.
        :type time_exceptions: bool
        """
        self.app = app
        self.statsd_client = client
        self.time_exceptions = time_exceptions

    def __call__(self, environ, start_response):
        """Call the application and time it.

        :param environ: Dictionary object, containing CGI-style environment variables.
        :param start_response: Callable used to begin the HTTP response.
        """
        interception = {}

        def start_response_wrapper(status, response_headers, exc_info=None):
            """Closure function to wrap the start_response in order to retrieve the status code."""
            interception['status'] = status
            return start_response(status, response_headers, exc_info)

        def send_stats():
            stop = time.time()
            if interception:
                # Now we can generate the key name.
                status = interception['status'].split()[0]  # Leave only the status code.
                key_name = '.'.join([environ['PATH_INFO'], environ['REQUEST_METHOD'], status])

                # Create the timer object and send the data to statsd.
                timer = self.statsd_client.timer(key_name)
                time_delta = stop - start
                timer.ms = int(round(1000 * time_delta))  # Convert to milliseconds.
                timer.send()

        # Time the call.
        start = time.time()
        try:
            response = self.app(environ, start_response_wrapper)
            for event in response:
                yield event
            if hasattr(response, 'close'):
                response.close()
            send_stats()
        except Exception:
            if self.time_exceptions:
                send_stats()
            raise
