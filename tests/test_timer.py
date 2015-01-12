"""Tests for the wsgi-statsd package."""

import mock
import six
from webtest import TestApp
from wsgi_statsd import StatsdTimingMiddleware


def application(environ, start_response):
    """Simple application for test purposes."""
    response_body = 'The request method was %s' % environ['REQUEST_METHOD']
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)

    if six.PY3:
        response = [bytes(response_body, 'utf-8')]
    else:
        response = [response_body]

    return response


@mock.patch('statsd.StatsClient')
def test_timer1(mock_client):
    """Test the timer functionality.

    Check the following:
    - timer.send() is called
    - timer.ms is not None
    - the key is generated as expected, i.e. PATH_INFO.REQUEST_METHOD.RESPONSE_CODE.
    """
    with mock.patch.object(mock_client, 'timer', autospec=True) as mock_timer:
        timed_app = StatsdTimingMiddleware(application, mock_client)
        app = TestApp(timed_app)
        app.get('/test')

    assert mock_timer.return_value.send.called
    assert mock_timer.return_value.ms is not None
    assert mock_timer.call_args[0] == ('/test.GET.200',)
