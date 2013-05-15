__author__ = 'Joe Linn'

class Shard(object):
    def __init__(self, shard_number, data):
        """
        @param shard_number: the shard index / number
        @type shard_number: int
        @param data: the shard health data
        @type data: dict
        """
        super(Shard, self).__init__()
        self._shard_number = shard_number
        self._data = data

    @property
    def shard_number(self):
        """
        Get the index / number of this shard
        @return:
        @rtype: int
        """
        return self._shard_number

    @property
    def status(self):
        """
        Get the status of this shard
        @return: green, yellow, or red
        @rtype: str
        """
        return self._data['status']

    def is_primary_active(self):
        """
        Is the primary active?
        @return:
        @rtype: bool
        """
        return bool(self._data['primary_active'])

    def is_active(self):
        """
        Is the shard active?
        @return:
        @rtype: bool
        """
        return bool(self._data['active_shards'])

    def is_relocating(self):
        """
        Is the shard relocating?
        @return:
        @rtype: bool
        """
        return bool(self._data['relocating_shards'])

    def is_initialized(self):
        """
        Is the shard initialized?
        @return:
        @rtype: bool
        """
        return bool(self._data['initializing_shards'])

    def is_unassigned(self):
        """
        Is the shard unassigned?
        @return:
        @rtype: bool
        """
        return bool(self._data['unassigned_shards'])
