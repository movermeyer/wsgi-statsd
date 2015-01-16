"""Tests for the wsgi-statsd package."""
import mock
import six
from webob import Response
from webob.response import AppIterRange

import pytest
from webtest import TestApp

from wsgi_statsd import StatsdTimingMiddleware


def application(environ, start_response):
    """Simple application for test purposes."""
    response_body = six.b('The request method was {0}'.format(environ['REQUEST_METHOD']))
    response_len = len(response_body)
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(response_len))]

    start_response(status, response_headers)

    return Response(
        app_iter=AppIterRange([response_body], 0, response_len), headerlist=response_headers).app_iter


def raising_application(environ, start_response):
    """Application which raises an exception."""
    application(environ, start_response)
    raise Exception()


@mock.patch('statsd.StatsClient')
def test_timer1(mock_client):
    """Test the timer functionality.

    Check the following:
    - timer.stop() is called
    - timer.ms is not None
    - the key is generated as expected, i.e. PATH_INFO.REQUEST_METHOD.RESPONSE_CODE.
    """
    with mock.patch.object(mock_client, 'timer', autospec=True) as mock_timer:
        timed_app = StatsdTimingMiddleware(application, mock_client)
        app = TestApp(timed_app)
        app.get('/test')

    assert mock_timer.return_value.stop.called
    assert mock_timer.return_value.ms is not None
    assert mock_timer.call_args[0] == ('test.GET.200',)


@mock.patch('statsd.StatsClient')
def test_response_not_altered(mock_client):
    """Assert that the response was not changed by the middleware."""
    timed_app = StatsdTimingMiddleware(application, mock_client)
    app = TestApp(timed_app)
    response = app.get('/test')

    assert response.body.decode() == u'The request method was GET'


@mock.patch.object(AppIterRange, 'close')
@mock.patch('statsd.StatsClient')
def test_close_called(mock_client, mock_close):
    """Assert that the response close is called when exists."""
    timed_app = StatsdTimingMiddleware(application, mock_client)
    app = TestApp(timed_app)
    app.get('/test')
    assert mock_close.called


@pytest.mark.parametrize('time_exceptions', [False, True])
@mock.patch.object(AppIterRange, 'close')
@mock.patch('statsd.StatsClient')
def test_exception_response(mock_client, mock_close, time_exceptions):
    """Assert that we time exceptions (during the response) depending on the time_exceptions param."""
    timed_app = StatsdTimingMiddleware(raising_application, mock_client, time_exceptions=time_exceptions)
    app = TestApp(timed_app)
    with mock.patch.object(mock_client, 'timer', autospec=True) as mock_timer:
        with pytest.raises(Exception):
            app.get('/test')
    assert mock_timer.return_value.stop.called == time_exceptions
    assert not mock_close.called
    if time_exceptions:
        assert mock_timer.call_args[0] == ('test.GET.200.Exception',)


@pytest.mark.parametrize('time_exceptions', [False, True])
@mock.patch.object(AppIterRange, 'close')
@mock.patch('statsd.StatsClient')
def test_exception_iter(mock_client, mock_close, monkeypatch, time_exceptions):
    """Assert that the response close is called when exists even if there's exception during the iteration."""
    mock_close.next_called = False

    def response_next(self):
        mock_close.next_called = True
        raise Exception()

    if six.PY3:
        monkeypatch.setattr(AppIterRange, '__next__', response_next)
    else:
        monkeypatch.setattr(AppIterRange, 'next', response_next)

    timed_app = StatsdTimingMiddleware(application, mock_client, time_exceptions=time_exceptions)
    app = TestApp(timed_app)
    with mock.patch.object(mock_client, 'timer', autospec=True) as mock_timer:
        with pytest.raises(Exception):
            app.get('/test')
    assert mock_close.called
    assert mock_close.next_called
    if time_exceptions:
        assert mock_timer.call_args[0] == ('test.GET.200.Exception',)
