__author__ = 'Joe Linn'


class Info(object):
    def __init__(self, node, params=None):
        """
        @param node:
        @type node: pylastica.node.Node
        @param params: list of parameters to return. (settings, os, process, jvm, thread_pool, network, transport, http)
        @type params: list of str
        """
        super(Info, self).__init__()
        import pylastica.node
        assert isinstance(node, pylastica.node.Node), "node must be of type pylastica.node.Node: %r" % node
        self._node = node
        self.refresh(params)

    def get(self, *args):
        """
        Returns an entry in the data array based on the args.
        Example: get('os', 'mem', 'total') returns total memory of the node's system
        Example: get('os', 'mem') returns a dict with all memory info for the node
        @param args:
        @type args: str
        @return: returns None if the requested data cannot be found
        @rtype: str or dict or None
        """
        data = self.data
        for arg in args:
            if arg in data:
                data = data[arg]
            else:
                return None
        return data

    @property
    def port(self):
        """
        Return the port of the node
        @return:
        @rtype: int
        """
        return self.get('http_address')[6:-7].split(':')[1]

    @property
    def ip(self):
        """
        Get the ip address of the node
        @return:
        @rtype: str
        """
        return self.get('http_address')[6:-7].split(':')[0]

    @property
    def data(self):
        """
        Return all info data
        @return:
        @rtype: dict
        """
        return self._data

    @property
    def node(self):
        """
        Return the Node object
        @return:
        @rtype: pylastica.node.Node
        """
        return self._node

    @property
    def response(self):
        """
        Return the Response object
        @return:
        @rtype: pylastica.response.Response
        """
        return self._response

    @property
    def plugins(self):
        """
        Return a list of the plugins installed on this node
        @return:
        @rtype: list of dict
        """
        if self._params is None or 'plugin' not in self._params:
            #plugins were not retrieved when refresh() was called last. Get them now.
            if isinstance(self._params, list):
                self._params.append('plugin')
            else:
                self._params = ['plugin']
            self.refresh(self._params)
        return self.get('plugins')

    def has_plugin(self, name):
        """
        Determine if the given plugin is installed on this node
        @param name: name of the plugin
        @type name: str
        @return:
        @rtype: bool
        """
        for plugin in self.plugins:
            if plugin['name'] == name:
                return True
        return False

    def refresh(self, params=None):
        """
        Reload all node information. Must be called if said information has changed
        @param params: params to return (defaults to none). (settings, os, process, jvm, thread_pool, network, transport, http)
        @type params: list of str
        @return:
        @rtype: pylastica.response.Response
        """
        self._params = params
        query = {param: True for param in params} if params is not None else None
        self._response = self.node.client.request("_cluster/nodes/%s" % self.node.name, query=query)
        data = self.response.data
        self._data = data['nodes'].items()[0][1]
