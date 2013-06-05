__author__ = 'Joe Linn'

import pylastica.exception


class ResponseException(pylastica.exception.BulkException):
    def __init__(self, response_set, *args, **kwargs):
        """

        @param response_set:
        @type response_set: pylastica.bulk.responseset.ResponseSet
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        assert isinstance(response_set, pylastica.bulk.responseset.ResponseSet), "response_set must be an instance of ResponseSet: %r" % response_set
        self._response_set = None
        self._action_exceptions = []
        self._init(response_set)
        message = "Error in one or more bulk request actions:\n\n"
        message += self.action_exceptions_as_string
        super(ResponseException, self).__init__(message, *args, **kwargs)

    def _init(self, response_set):
        """

        @param response_set:
        @type response_set: pylastica.bulk.responseset.ResponseSet
        @return:
        @rtype: void
        """
        self._response_set = response_set
        for bulk_response in response_set.bulk_responses:
            if bulk_response.has_error():
                self._action_exceptions.append(pylastica.exception.bulk.response.ActionException(bulk_response))

    @property
    def response_set(self):
        """

        @return:
        @rtype: pylastica.bulk.responseset.ResponseSet
        """
        return self._response_set

    @property
    def failures(self):
        """

        @return:
        @rtype: list of str
        """
        return [str(action_exception) for action_exception in self.action_exceptions]

    @property
    def action_exceptions(self):
        """

        @return:
        @rtype: list of pylastica.exception.bulk.response.ActionException
        """
        return self._action_exceptions

    @property
    def action_exceptions_as_string(self):
        """

        @return:
        @rtype: str
        """
        message = ''
        for action_exception in self.action_exceptions:
            message += str(action_exception) + "\n"
        return message

from . import response
