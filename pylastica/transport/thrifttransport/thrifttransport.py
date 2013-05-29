__author__ = 'Joe Linn'

import json
import thrift
import thrift.transport
import thrift.transport.TSocket
import thrift.protocol
import Rest
from pylastica.transport import AbstractTransport
import pylastica.response
import pylastica.exception.connection


class ThriftTransport(AbstractTransport):
    def __init__(self, connection=None):
        """
        @param connection:
        @type connection:  pylastica.connection.Connection
        """
        super(ThriftTransport, self).__init__(connection)
        self._clients = {}

    def _create_client(self, host, port, send_timeout=None, recv_timeout=None, framed_transport=False):
        """

        @param host: hostname / ip address
        @type host: str
        @param port:
        @type port: int
        @param send_timeout: milliseconds
        @type send_timeout: int
        @param recv_timeout: milliseconds
        @type recv_timeout: int
        @param framed_transport:
        @type framed_transport: bool
        @return:
        @rtype: Rest.Client
        """
        socket = thrift.transport.TSocket.TSocket(host, port)
        if send_timeout is not None:
            socket.setSendTimeout(send_timeout)
        if recv_timeout is not None:
            socket.setRecvTimeout(recv_timeout)
        if framed_transport:
            transport = thrift.transport.TTransport.TFramedTransport(socket)
        else:
            transport = thrift.transport.TTransport.TBufferedTransport(socket)
        protocol = thrift.protocol.TBinaryProtocol.TBinaryProtocolAccelerated(transport)
        client = Rest.Client(protocol)
        transport.open()
        return client

    def _get_client(self, host, port, send_timeout=None, recv_timeout=None, framed_transport=False):
        """

        @param host: hostname / ip address
        @type host: str
        @param port:
        @type port: int
        @param send_timeout: milliseconds
        @type send_timeout: int
        @param recv_timeout: milliseconds
        @type recv_timeout: int
        @param framed_transport:
        @type framed_transport: bool
        @return:
        @rtype: Rest.Client
        """
        key = "%s:%s" % (host, port)
        if key not in self._clients:
            self._clients[key] = self._create_client(host, port, send_timeout, recv_timeout, framed_transport)
        return self._clients[key]

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
        send_timeout = int(connection.get_config('send_timeout')) if connection.has_config('send_timeout') else None
        recv_timeout = int(connection.get_config('recv_timeout')) if connection.has_config('recv_timeout') else None
        framed_transport = bool(connection.get_config('framed_transport')) if connection.has_config('framed_transport') else False
        try:
            client = self._get_client(connection.host, connection.port, send_timeout, recv_timeout, framed_transport)
            rest_request = Rest.RestRequest()
            rest_request.method = Rest.Method._NAMES_TO_VALUES[request.get_method()]
            rest_request.uri = request.path

            query = request.query
            if query is not None:
                rest_request.parameters = query
            data = request.get_data()
            if data is not None:
                if isinstance(data, dict):
                    content = json.dumps(data)
                else:
                    content = data
                rest_request.body = content
            result = client.execute(rest_request)
            response = pylastica.response.Response(result.body)
        except thrift.Thrift.TException as e:
            response = pylastica.response.Response('')
            raise pylastica.exception.connection.ThriftException(e, request, response)
        if response.has_error():
            raise pylastica.exception.ResponseException(request, response)
        return response
