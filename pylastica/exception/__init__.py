__author__ = 'Joe Linn'

import abc
import pylastica.response


class AbstractException(Exception):
    __metaclass__ = abc.ABCMeta


class BulkException(AbstractException):
    pass


class ClientException(AbstractException):
    pass


class ConnectionException(AbstractException):
    def __init__(self, message, request=None, response=None, *args, **kwargs):
        """

        @param message:
        @type message: str
        @param request:
        @type request: pylastica.request.Request
        @param response:
        @type response: pylastica.response.Response
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        """
        if request is not None:
            assert isinstance(request, pylastica.Request), "request must be an instance of Request: %r" % request
        if response is not None:
            assert isinstance(response, pylastica.response.Response), "response must be an instance of Response: %r" % response
        self._request = request
        self._response = response
        super(ConnectionException, self).__init__(message, *args, **kwargs)

    @property
    def request(self):
        """

        @return:
        @rtype: pylastica.request.Request
        """
        return self._request

    @property
    def response(self):
        """

        @return:
        @rtype: pylastica.response.Response
        """
        return self._response


class InvalidException(AbstractException):
    pass


class NotFoundException(AbstractException):
    pass


class NotImplementedException(AbstractException):
    pass


class ResponseException(AbstractException):
    def __init__(self, request, response, *args, **kwargs):
        """

        @param request:
        @type request: pylastica.request.Request
        @param response:
        @type response: pylastica.response.Response
        """
        self._request = request
        self._response = response
        super(ResponseException, self).__init__(response.get_error(), *args, **kwargs)

    @property
    def request(self):
        """

        @return:
        @rtype: pylastica.request.Request
        """
        return self._request

    @property
    def response(self):
        """

        @return:
        @rtype: pylastica.response.Response
        """
        return self._response


class RuntimeException(AbstractException):
    pass