__author__ = 'Joe Linn'

import json
import pylastica.exception


class Response(object):
    def __init__(self, response_string):
        """
        @param response_string: response string (json)
        @type response_string: str or dict
        """
        self._query_time = None
        self._response_string = ''
        self._error = False
        self._transfer_info = {}
        self._response = None
        if isinstance(response_string, dict):
            self._response = response_string
        else:
            self._response_string = response_string

    @property
    def status(self):
        """
        Get the HTTP status code for this response
        @return:
        @rtype: str
        """
        status = ''
        response = self.data
        if 'status' in response:
            status = response['status']
        return str(status)

    def get_error(self):
        """
        Error message
        @return:
        @rtype: str
        """
        message = ''
        response = self.get_data()
        if 'error' in response:
            message = response['error']
        return message

    @property
    def error(self):
        """

        @return:
        @rtype: str
        """
        return self.get_error()

    def has_error(self):
        """
        Determine if the response has an error
        @return: True if error, False otherwise
        @rtype: bool
        """
        response = self.get_data()
        if 'error' in response:
            return True
        return False

    def is_ok(self):
        """
        Check if the query returned ok
        @return:
        @rtype: bool
        """
        data = self.get_data()
        #bulk insert checks
        if 'items' in data:
            for item in data['items']:
                if not item['index']['ok']:
                    return False
            return True
        return 'ok' in data and data['ok']

    def get_data(self):
        """
        Response data dict
        @return:
        @rtype: dict
        """
        if self._response is None:
            response = self._response_string
            if response == False:
                self._error = True
            else:
                temp_response = json.loads(response)
                #TODO: see what happens here if an error is returned
                if temp_response is not None:
                    response = temp_response
            if response is None or response == '':
                response = {}
            if isinstance(response, str):
                response = {'message': response}
            self._response = response
        return self._response

    @property
    def data(self):
        """
        Response data dict
        @return:
        @rtype: dict
        """
        return self.get_data()

    def get_transfer_info(self):
        """
        Get the transfer information if in DEBUG mode
        @return:
        @rtype: dict
        """
        return self._transfer_info

    def set_transfer_info(self, transfer_info):
        """
        Set the transfer info of the curl request. This is only used in DEBUG mode.
        @param transfer_info:
        @type transfer_info: dict
        @return:
        @rtype: self
        """
        self._transfer_info = transfer_info
        return self

    def get_query_time(self):
        """
        Only available if DEBUG mode is enabled
        @return:
        @rtype: float
        """
        return self._query_time

    def set_query_time(self, query_time):
        """
        Set query time
        @param query_time:
        @type query_time: float
        @return:
        @rtype: self
        """
        self._query_time = query_time
        return self

    def get_engine_time(self):
        """
        Time taken by the request
        @return:
        @rtype: int
        """
        data = self.get_data()
        if 'took' not in data:
            raise pylastica.exception.NotFoundException("unable to find the field 'took' in the response.")
        return data['took']

    def get_shard_statistics(self):
        """
        Get the _shard statistics for the response
        @return:
        @rtype: dict
        """
        data = self.get_data()
        if '_shards' not in data:
            raise pylastica.exception.NotFoundException("Unable to find the field '_shards' in the response.")
        return data['_shards']

    @property
    def scroll_id(self):
        """
        Get the _scroll value for the response
        @return:
        @rtype: str
        """
        data = self.data
        if '_scroll_id' not in data:
            raise pylastica.exception.NotFoundException("unable to find the field '_scroll_id' in the response.")
        return data['_scroll_id']
