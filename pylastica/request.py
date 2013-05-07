__author__ = 'Joe Linn'

import json
#import pylastica
import pylastica.param

class Request(pylastica.param.Param):
    POST = 'POST'
    PUT = 'PUT'
    GET = 'GET'
    DELETE = 'DELETE'

    def __init__(self, path, method='GET', data=None, query=None, connection=None):
        """
        @param path: Request path
        @type path: str
        @param method: optional request method (use class properties)
        @type method: str
        @param data: optional request data
        @type data: dict
        @param query: optional query params
        @type query: dict
        @param connection: optional connection object
        @type connection: pylastica.connection.Connection
        """
        super(Request, self).__init__()
        self._connection = None
        if not query: query = {}
        if not data: data = {}
        self.set_path(path)
        self.set_method(method)
        self.set_data(data)
        self.set_query(query)
        if connection is not None:
            self.set_connection(connection)

    def set_method(self, method):
        """
        Set the request method. Use one of the class properties.
        @param method: request method
        @type method: str
        @return:
        @rtype: self
        """
        return self.set_param('method', method)

    def get_method(self):
        """
        Get the request method
        @return:
        @rtype: str
        """
        return self.get_param('method')

    def set_data(self, data):
        """
        Set the request data
        @param data:
        @type data: dict
        @return:
        @rtype: self
        """
        return self.set_param('data', data)

    def get_data(self):
        """
        Get request data
        @return:
        @rtype: dict
        """
        return self.get_param('data')

    def set_path(self, path):
        """
        Set the request path
        @param path:
        @type path: str
        @return:
        @rtype: self
        """
        return self.set_param('path', path)

    def get_path(self):
        """
        Get the request path
        @return:
        @rtype: str
        """
        return self.get_param('path')

    @property
    def path(self):
        """

        @return:
        @rtype: str
        """
        return self.get_path()

    @path.setter
    def path(self, path):
        """

        @param path:
        @type path: str
        """
        self.set_path(path)

    def set_query(self, query):
        """

        @param query:
        @type query: dict
        @return:
        @rtype: self
        """
        return self.set_param('query', query)

    def get_query(self):
        """
        Retrun query params
        @return:
        @rtype: dict
        """
        return self.get_param('query')

    @property
    def query(self):
        """

        @return:
        @rtype: dict
        """
        return self.get_query()

    @query.setter
    def query(self, query):
        """

        @param query:
        @type query: dict
        """
        self.set_query(query)

    def set_connection(self, connection):
        """

        @param connection:
        @type connection: pylastica.connection.Connection
        @return:
        @rtype: self
        """
        assert isinstance(connection, pylastica.connection.Connection), "connection must be of type Connection: %r" % connection
        self._connection = connection
        return self

    def get_connection(self):
        """
        Return Connection object
        @return:
        @rtype: pylastica.connection.Connection
        """
        if self._connection is None:
            raise pylastica.exception.InvalidException("No valid connection object set.")
        return self._connection

    def send(self):
        """
        Send a request to the server
        @return:
        @rtype: pylastica.response.Response
        """
        transport = self.get_connection().get_transport_object()
        return transport.execute(self, self.get_connection().to_dict())

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        data = self.params
        if self._connection is not None:
            data['connection'] = self._connection.get_params()
        return data

    def to_str(self):
        """
        Convert request to curl request format
        @return:
        @rtype: str
        """
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_str()
