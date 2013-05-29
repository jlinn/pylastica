__author__ = 'Joe Linn'


class Stats(object):
    def __init__(self, node):
        """
        @param node:
        @type node: pylastica.node.Node
        """
        super(Stats, self).__init__()
        import pylastica.node
        assert isinstance(node, pylastica.node.Node), "node must be an instance of pylastica.node.Node: %r" % node
        self._node = node
        self.refresh()

    def get(self, *args):
        """
        Returns an entry in the data array based on the args.
        Example: get('index', 'test', 'example')
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
    def data(self):
        """
        Returns all stats data
        @return:
        @rtype: dict
        """
        return self._data

    @property
    def node(self):
        """
        Returns the node object
        @return:
        @rtype: pylastica.node.Node
        """
        return self._node

    @property
    def response(self):
        """
        Returns the Response object
        @return:
        @rtype: pylastica.response.Response
        """
        return self._response

    def refresh(self):
        """
        Reloads all node information
        @return:
        @rtype: pylastica.response.Response
        """
        self._response = self.node.client.request('_cluster/nodes/%s/stats' % self.node.name)
        self._data = self.response.data['nodes']
