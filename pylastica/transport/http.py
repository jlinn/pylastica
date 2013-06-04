__author__ = 'Joe Linn'

import urllib3
import json
import pylastica.transport
import pylastica.exception.connection


class Http(pylastica.transport.AbstractTransport):
    _scheme = 'http'

    METHOD_GET = 'GET'
    METHOD_POST = 'POST'
    METHOD_PUT = 'PUT'
    METHOD_DELETE = 'DELETE'

    def __init__(self, connection=None):
        super(Http, self).__init__(connection)
        self._headers = {}

    def execute(self, request, params):
        """
        Executes a transport request
        @param request: request object
        @type request: pylastica.request.Request
        @param params: hostname, port, path, etc.
        @type params: dict
        @return:
        @rtype: pylastica.response.Response
        """
        connection = self.connection
        url = connection.get_config('url') if connection.has_config('url') else ''
        if url != '' and url is not None:
            base_url = url
        else:
            connection_data = {
                'scheme': self._scheme,
                'host': connection.host,
                'port': connection.port,
                'path': connection.path
            }
            base_url = "%(scheme)s://%(host)s:%(port)s/%(path)s" % connection_data
        base_url += request.path
        query = request.query #http query params
        if connection.has_config('headers'):
            for key, value in connection.get_config('headers'):
                self.setHeader(key, value)
        data = request.get_data()
        http_method = request.get_method()
        content = None
        if data is not None:
            if self.has_param('postWithRequestBody') and self.get_param('postWithRequestBody'):
                http_method = self.METHOD_POST
            if isinstance(data, dict) or isinstance(data, list):
                content = json.dumps(data)
            else:
                content = data
        #TODO: something for debugging
        response = self.request(http_method, base_url, query, content)
        response_object = pylastica.response.Response(response.data)
        return response_object

    def setHeader(self, key, value):
        """
        Set a HTTP header. Will overwrite any existing value with the same key.
        @param key: The key of the header
        @type key: str
        @param value: The value of the header
        @type value: str
        @return: self
        @rtype: Http
        """
        self._headers[key] = value
        return self

    def clearHeaders(self):
        """
        Clear currently set header data
        @return:
        @rtype: void
        """
        self._headers = {}

    def get(self, url, query_params={}, data=None):
        """

        @param url: full-qualified URL
        @param query_params: any query parameters to be sent along with the URL
        @param data: request data to be sent
        @return: results of the HTTP GET request
        """
        return self.request(self.METHOD_GET, url, query_params, data)

    def post(self, url, query_params={}, data=None):
        """

        @param url:
        @type url: str
        @param query_params:
        @type query_params: dict
        @param data:
        @type data: str
        @return:
        @rtype: str
        """
        return self.request(self.METHOD_POST, url, query_params, data)

    def put(self, url, query_params={}, data=None):
        """

        @param url:
        @type url: str
        @param query_params:
        @type query_params: dict
        @param data:
        @type data: str
        @return: str
        @rtype:
        """
        return self.request(self.METHOD_PUT, url, query_params, data)

    def delete(self, url, query_params={}, data=None):
        """

        @param url:
        @type url: str
        @param query_params:
        @type query_params: dict
        @param data:
        @type data: str
        @return:
        @rtype: str
        """
        return self.request(self.METHOD_DELETE, url, query_params, data)

    def request(self, method, url, query_params=None, data=None):
        """
        @param method: HTTP method (see METHOD_* constants)
        @type method: str
        @param url:
        @type url: str
        @param query_params:
        @type query_params: dict
        @param data:
        @type data: str
        @return:
        @rtype: urllib3.response.HTTPResponse
        """
        http = urllib3.PoolManager()
        try:
            response = http.request_encode_url(method, url, fields=query_params, body=data, headers=self._headers)
        except urllib3.exceptions.MaxRetryError as e:
            raise pylastica.exception.connection.HttpException(e)
        return response
