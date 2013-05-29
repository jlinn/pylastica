__author__ = 'Joe Linn'

import pylastica.exception

class HttpException(pylastica.exception.ConnectionException):
    def __init__(self, error, request=None, response=None):
        """

        @param error:
        @type error: str
        @param request:
        @type request: pylastica.request.Request
        @param response:
        @type response: pylastica.response.Response
        """
        self._error = error
        message = self.get_error_message(self.error)
        super(HttpException, self).__init__(message, request, response)

    def get_error_message(self, error):
        """
        Returns the error message corresponding to the error code
        @param error: error code
        @type error: str
        @return: error message
        @rtype: str
        """
        #TODO: translate http error codes
        return error

    @property
    def error(self):
        """

        @return:
        @rtype: str
        """
        return self._error

class ThriftException(pylastica.exception.ConnectionException):
    def __init__(self, thrift_exception, request=None, response=None, *args, **kwargs):
        """

        @param thrift_exception:
        @type thrift_exception: thrift.Thrift.TException
        @param request:
        @type request: pylastica.request.Request
        @param response:
        @type response: pylastica.response.Response
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        """
        self._thrift_exception = thrift_exception
        message = self.error_message
        super(ThriftException, self).__init__(message, request, response, *args, **kwargs)

    @property
    def error_message(self):
        """

        @return:
        @rtype: str
        """
        return self.thrift_exception.message

    @property
    def thrift_exception(self):
        """

        @return:
        @rtype: thrift.Thrift.TException
        """
        return self._thrift_exception
