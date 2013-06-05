__author__ = 'Joe Linn'

import pylastica.exception


class ActionException(pylastica.exception.BulkException):
    def __init__(self, response, *args, **kwargs):
        """

        @param response:
        @type response: pylastica.bulk.response.Response
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        self._response = response
        super(ActionException, self).__init__(self.get_error_message(response), *args, **kwargs)

    @property
    def action(self):
        """

        @return:
        @rtype: pylastica.bulk.action.Action
        """
        return self.response.action

    @property
    def response(self):
        """

        @return:
        @rtype: pylastica.bulk.response.Response
        """
        return self._response

    def get_error_message(self, response):
        """

        @param response:
        @type response: pylastica.bulk.response.Response
        @return:
        @rtype: str
        """
        error = response.error
        op_type = response.op_type
        data = response.data
        path = ''
        if '_index' in data:
            path += '/' + data['_index']
        if '_type' in data:
            path += '/' + data['_type']
        if '_id' in data:
            path += '/' + data['_id']
        return "%s: %s caused %s" % (op_type, path, error)
