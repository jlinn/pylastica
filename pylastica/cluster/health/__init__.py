__author__ = 'Joe Linn'

from .index import *
from .shard import *

class Health(object):
    def __init__(self, client):
        """
        @param client:
        @type client: pylastica.client.Client
        """
        super(Health, self).__init__()
        self._client = client
        self.refresh()
        self._data = None

    def _retrieve_health_data(self):
        """
        Retrieves health data from the cluster
        @return:
        @rtype: dict
        """
        return self._client.request('_cluster/health', query={'level': 'shards'}).data

    @property
    def data(self):
        """
        Get the health data
        @return:
        @rtype: dict
        """
        return self._data

    def refresh(self):
        """
        Refresh the health data of the cluster
        @return:
        @rtype: self
        """
        self._data = self._retrieve_health_data()
        return self

    @property
    def cluster_name(self):
        """
        Get the name of the cluster
        @return:
        @rtype: str
        """
        return self._data['cluster_name']

    @property
    def status(self):
        """
        Get the status of the cluster
        @return: green, yellow, or red
        @rtype: str
        """
        return self._data['status']

    @property
    def timed_out(self):
        """

        @return:
        @rtype: bool
        """
        return bool(self._data['timed_out'])

    @property
    def number_of_nodes(self):
        """
        Get the number of nodes in the cluster
        @return:
        @rtype: int
        """
        return int(self._data['number_of_nodes'])

    @property
    def number_of_data_nodes(self):
        """
        Get the number of data nodes in the cluster
        @return:
        @rtype: int
        """
        return int(self._data['number_of_data_nodes'])

    @property
    def active_primary_shards(self):
        """
        Get the number of active primary shards
        @return:
        @rtype: int
        """
        return int(self._data['active_primary_shards'])

    @property
    def active_shards(self):
        """
        Get the number of active shards
        @return:
        @rtype: int
        """
        return int(self._data['active_shards'])

    @property
    def relocating_shards(self):
        """
        Get the number of relocating shards
        @return:
        @rtype: int
        """
        return int(self._data['relocating_shards'])

    @property
    def initializing_shards(self):
        """
        Get the number of initializing shards
        @return:
        @rtype: int
        """
        return int(self._data['initializing_shards'])

    @property
    def unassigned_shards(self):
        """
        Get the number of unassigned shards
        @return:
        @rtype: int
        """
        return int(self._data['unassigned_shards'])

    @property
    def inidices(self):
        """
        Get the status of the indices
        @return:
        @rtype: pylastica.cluster.health.index.Index
        """
        return [Index(name, index) for name, index in self._data['indices'].iteritems()]
