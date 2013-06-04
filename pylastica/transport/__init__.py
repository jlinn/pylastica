__author__ = 'Joe Linn'

import abc
import copy
import pylastica.param
import pylastica.util


class AbstractTransport(pylastica.param.Param):
    __metaclass__ = abc.ABCMeta

    def __init__(self, connection=None):
        """
        @param connection:
        @type connection:  pylastica.connection.Connection
        """
        super(AbstractTransport, self).__init__()
        self._connection = None
        if connection is not None:
            self.connection = connection

    @property
    def connection(self):
        """

        @return:
        @rtype: pylastica.connection.Connection
        """
        return self._connection

    @connection.setter
    def connection(self, connection):
        """

        @param connection:
        @type connection: pylastica.connection.Connection
        """
        assert isinstance(connection, pylastica.connection.Connection), "connection must be a Connection object: %r" % connection
        self._connection = connection

    @abc.abstractmethod
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
        pass

    @classmethod
    def create(cls, transport, connection, params=None):
        """
        Create a transport
        @param cls:
        @type cls:
        @param transport: can be the name of a transport ('Http', 'Memcache', etc.), a transport object, or a dict
        @type transport: str or AbstractTransport or dict
        @param connection:
        @type connection: pylastica.connection.Connection
        @param params: parameters for the transport class
        @type params: dict
        @return:
        @rtype: cls
        """
        if isinstance(transport, dict) and 'type' in transport:
            transport_params = copy.deepcopy(transport)
            del transport_params['type']
            if params is None:
                params = {}
            params.update(transport_params)
            transport = transport['type']
        if isinstance(transport, str):
            class_name = 'pylastica.transport.%s' % transport
            transport = pylastica.util.get_class(class_name)()
        if isinstance(transport, AbstractTransport):
            transport.connection = connection
            if params:
                for key, value in params.iteritems():
                    transport.set_param(key, value)
        else:
            raise pylastica.exception.InvalidException("Invalid transport.")
        return transport

