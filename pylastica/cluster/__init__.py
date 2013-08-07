__author__ = 'Joe Linn'

import pylastica.client
import pylastica.request
from . import health
from .settings import *

class Cluster(object):
    def __init__(self, client):
        """

        @param client:
        @type client: pylastica.client.Client
        """
        super(Cluster, self).__init__()
        assert isinstance(client, pylastica.client.Client), "client must be an instance of pylastica.client.Client: %r" % client
        self._client = client
        self._response = None
        self._data = None
        self.refresh()

    def refresh(self):
        """
        Refresh all cluster information
        @return:
        @rtype: self
        """
        self._response = self._client.request('_cluster/state', pylastica.request.Request.GET)
        self._data = self.response.data

    @property
    def pending_tasks(self):
        """
        Get a list of pending cluster tasks
        @return:
        @rtype: pylastica.response.Response
        """
        return self._client.request('_cluster/pending_tasks')

    @property
    def response(self):
        """
        Return the Response object
        @return:
        @rtype: pylastica.response.Response
        """
        return self._response

    @property
    def index_names(self):
        """
        Return a list of index names
        @return:
        @rtype: list of str
        """
        metadata = self._data['metadata']['indices']
        return [key for key in metadata]

    @property
    def state(self):
        """
        Returns the full state of the cluster
        @return:
        @rtype: dict
        @see: http://www.elasticsearch.org/guide/reference/api/admin-cluster-state.html
        """
        return self._data

    @property
    def node_names(self):
        """
        Returns a list of existing node names
        @return:
        @rtype: list of str
        """
        return self.state['routing_nodes']['nodes'].keys()

    @property
    def nodes(self):
        """
        Return all nodes in the cluster
        @return:
        @rtype: list of pylastica.node.Node
        """
        return [pylastica.node.Node(name, self.client) for name in self.node_names]

    @property
    def client(self):
        """
        Return the client object
        @return:
        @rtype: pylastica.client.Client
        """
        return self._client

    def get_info(self, args = None):
        """
        Returns cluster information
        @param args: additional arguments
        @type args: dict
        @return:
        @rtype:
        @see: http://www.elasticsearch.org/guide/reference/api/admin-cluster-nodes-info.html
        """
        return self.client.request('_nodes', query=args)

    @property
    def health(self):
        """
        Return cluster health
        @return:
        @rtype: pylastica.cluster.health.Health
        """
        return pylastica.cluster.health.Health(self.client)

    @property
    def settings(self):
        """
        Return cluster settings
        @return:
        @rtype: pylastica.cluster.settings.Settings
        """
        return pylastica.cluster.settings.Settings(self.client)

    def shutdown(self, delay='1s'):
        """
        Shut down the cluster
        @param delay: (optional) time delay before cluster shutdown (default 1s)
        @type delay: str
        @return:
        @rtype: pylastica.response.Response
        """
        return self.client.request('_shutdown', query={'delay': delay})
