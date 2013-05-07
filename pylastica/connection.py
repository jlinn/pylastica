__author__ = 'Joe Linn'

#import pylastica
import pylastica.param
import pylastica.transport

class Connection(pylastica.param.Param):
    DEFAULT_PORT = 9200
    DEFAULT_HOST = 'localhost'
    DEFAULT_TRANSPORT = 'Http'
    TIMEOUT = 300

    def __init__(self, params=None):
        """

        @param params: optional connection params (host, port, transport, timeout, etc.)
        @type params: dict
        """
        super(Connection, self).__init__()
        self.params = params
        self.enabled = True
        if not self.has_param('config'):
            self.set_param('config', {})

    @property
    def port(self):
        """

        @return:
        @rtype: int
        """
        return self.get_param('port') if self.has_param('port') and self.get_param('port') is not None else self.DEFAULT_PORT

    @port.setter
    def port(self, port):
        """

        @param port:
        @type port: int
        """
        self.set_param('port', int(port))

    @property
    def host(self):
        """

        @return:
        @rtype: str
        """
        return self.get_param('host') if self.has_param('host') else self.DEFAULT_HOST

    @host.setter
    def host(self, host):
        """

        @param host:
        @type host: str
        """
        self.set_param('host', host)

    @property
    def transport(self):
        """

        @return:
        @rtype: str or dict
        """
        return self.get_param('transport') if self.has_param('transport') and self.get_param('transport') is not None else self.DEFAULT_TRANSPORT

    @transport.setter
    def transport(self, transport):
        """
        @param transport:
        @type transport: str
        """
        self.set_param('transport', transport)

    @property
    def path(self):
        """

        @return:
        @rtype: str
        """
        return self.get_param('path') if self.has_param('path') and self.get_param('path') is not None else ''

    @path.setter
    def path(self, path):
        """

        @param path:
        @type path: str
        """
        self.set_param('path', path)

    @property
    def timeout(self):
        """

        @return: connection timeout in seconds
        @rtype: int
        """
        return int(self.get_param('timeout')) if self.has_param('timeout') and self.get_param('timeout') is not None else self.TIMEOUT

    @timeout.setter
    def timeout(self, timeout):
        """

        @param timeout:
        @type timeout: int
        """
        self.set_param('timeout', int(timeout))

    @property
    def enabled(self):
        """

        @return:
        @rtype: bool
        """
        return bool(self.get_param('enabled'))

    @enabled.setter
    def enabled(self, enabled):
        """

        @param enabled:
        @type enabled: bool
        """
        self.set_param('enabled', bool(enabled))

    def is_enabled(self):
        """

        @return:
        @rtype: bool
        """
        return self.enabled

    def get_transport_object(self):
        """
        Returns an instance of the transport type
        @return:
        @rtype: pylastica.transport.AbstractTransport
        """
        return pylastica.transport.AbstractTransport.create(self.transport, self)

    def is_persistent(self):
        """

        @return: True if connection is persistent (default)
        @rtype: bool
        """
        return bool(self.get_param('persistent')) if self.has_param('persistent') else True

    def set_config(self, config):
        """

        @param config:
        @type config: dict
        @return:
        @rtype: self
        """
        return self.set_param('config', config)

    def add_config(self, key, value):
        """

        @param key:
        @type key: str
        @param value:
        @type value: mixexd
        @return:
        @rtype: self
        """
        self._params['config'][key] = value
        return self

    def has_config(self, key):
        """

        @param key:
        @type key: str
        @return:
        @rtype: bool
        """
        return key in self.get_config()

    def get_config(self, key=None):
        """
        Returns a specific config key or the whole config dict
        @param key:
        @type key: str
        @return: config value(s)
        @rtype: dict or str
        """
        config = self.get_param('config')
        if key is None:
            return config
        if key not in config:
            raise pylastica.exception.InvalidException("Config key %s is not set." % key)
        return config[key]

    @classmethod
    def create(cls, params=None):
        """

        @param cls:
        @type cls:
        @param params: params to create a connection
        @type params: dict or pylastica.connection.Connection
        @return:
        @rtype: cls
        """
        connection = None
        if isinstance(params, Connection):
            connection = params
        elif isinstance(params, dict):
            connection = cls(params)
        else:
            raise pylastica.exception.InvalidException('Invalid connection params: %r' % params)
        return connection
