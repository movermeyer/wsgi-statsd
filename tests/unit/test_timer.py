# -*- coding: utf-8 -*-
""""""
__author__ = 'Wouter Lansu'

import mock
from webtest import TestApp
from wsgi_statsd import StatsdTimingMiddleware


def application(environ, start_response):
    response_body = 'The request method was %s' % environ['REQUEST_METHOD']
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)

    return [response_body]


@mock.patch('statsd.StatsClient')
def test_timer(mock_client):
    """Test the timer functionality.

    Checks that the key is stored as expected, i.e. PATH_INFO + . + REQUEST_METHOD.
    """
    timed_app = StatsdTimingMiddleware(application, mock_client)
    app = TestApp(timed_app)
    app.get('/test')

    assert mock_client.timer.call_args[0] == ('/test.GET',)

