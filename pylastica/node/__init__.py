__author__ = 'Joe Linn'

import pylastica.client
from .info import *
from .stats import *


class Node(object):
    def __init__(self, name, client):
        """
        @param name: node name
        @type name: str
        @param client:
        @type client: pylastica.client.Client
        """
        super(Node, self).__init__()
        assert isinstance(client, pylastica.client.Client), "client must be an instance of pylastica.client.Client: %r" % client
        self._name = name
        self._client = client
        self.refresh()

    @property
    def name(self):
        """
        Get the name ofthe node
        @return:
        @rtype: str
        """
        return self._name

    @property
    def client(self):
        """
        Get the client object
        @return:
        @rtype: pylastica.client.Client
        """
        return self._client

    @property
    def stats(self):
        """
        Return stats object for the current node
        @return:
        @rtype: pylastica.node.stats.Stats
        """
        if not self._stats:
            self._stats = Stats(self)
        return self._stats

    @property
    def info(self):
        """
        Return an info object for the current node
        @return:
        @rtype: pylastica.node.info.Info
        """
        if not self._info:
            self._info = Info(self)
        return self._info

    def refresh(self):
        """
        Refresh node information. This should be called after updating a node.
        @return:
        @rtype: self
        """
        self._stats = None
        self._info = None
        return self

    def shutdown(self, delay='1s'):
        """
        Shut down this node.
        @param delay: (optional) Delay after which the node will be shut down. Defaults to 1s
        @type delay: str
        @return:
        @rtype: pylastica.response.Response
        """
        path = "_cluster/nodes/%s/_shutdown" % self.name
        return self.client.request(path, pylastica.request.Request.POST, query={'delay': delay})
