__author__ = 'Joe Linn'

from .shard import *

class Index(object):
    def __init__(self, name, data):
        """

        @param name: name of the index
        @type name: str
        @param data: index health data
        @type data: dict
        """
        super(Index, self).__init__()
        self._name = name
        self._data = data

    @property
    def name(self):
        """
        @return: the name of the index
        @rtype: str
        """
        return self._name

    @property
    def status(self):
        """
        Get the status of the index
        @return: green, yellow, or read
        @rtype: str
        """
        return self._data['status']

    @property
    def number_of_shards(self):
        """
        Get the number of shards in the index
        @return:
        @rtype: int
        """
        return int(self._data['number_of_shards'])

    @property
    def number_of_replicas(self):
        """
        Get the number of replicas
        @return:
        @rtype: int
        """
        return int(self._data['number_of_replicas'])

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
    def shards(self):
        """
        Get the health of the shards in this index
        @return:
        @rtype: list of pylastica.cluster.health.Shard
        """
        return [Shard(number, shard) for number, shard in self._data['shards'].iteritems()]
