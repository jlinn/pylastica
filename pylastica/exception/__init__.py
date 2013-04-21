__author__ = 'Joe Linn'

import abc

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
        self._request = request
        self._response = response
        super(ConnectionException, self).__init__(*args, **kwargs)

    def get_request(self):
        """

        @return:
        @rtype:
        """
        #TODO: finish this class

class InvalidException(AbstractException):
    pass

class NotFoundException(AbstractException):
    pass

class NotImplementedException(AbstractException):
    pass

#TODO: ResponseException

class RuntimeException(AbstractException):
    pass
