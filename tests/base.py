__author__ = 'Joe Linn'

import pylastica

class Base(object):
    def _get_client(self):
        """

        @return:
        @rtype: pylastica.Client
        """
        return pylastica.Client('es1.vr')

    def _create_index(self, name='test'):
        """
        Create a test index
        @param name: name of the index
        @type name: str
        @return:
        @rtype: pylastica.index.Index
        """
        client = self._get_client()
        index = client.get_index("pylastica_%s" % name)
        index.create({'index': {'number_of_shards': 1, 'number_of_replicas': 0}}, True)
        return index
