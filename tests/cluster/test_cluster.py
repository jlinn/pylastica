__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class ClusterTest(unittest.TestCase, Base):
    def test_get_node_names(self):
        client = self._get_client()
        cluster = pylastica.cluster.Cluster(client)
        names = cluster.node_names
        for name in names:
            self.assertIsInstance(name, unicode)
        self.assertGreater(len(names), 0)

    def test_get_nodes(self):
        client = self._get_client()
        cluster = client.cluster
        nodes = cluster.nodes
        for node in nodes:
            self.assertIsInstance(node, pylastica.node.Node)
        self.assertGreater(len(nodes), 0)

    def test_get_state(self):
        state = self._get_client().cluster.state
        self.assertIsInstance(state, dict)

    def test_get_index_names(self):
        cluster = self._get_client().cluster
        index = self._create_index('test999')
        index_name = index.name
        index.delete()
        cluster.refresh()

        #ensure that the index does not exist
        index_names = cluster.index_names
        self.assertFalse(index_name in index_names)

        index = self._create_index('test999')
        cluster.refresh()

        #index name should now be in the list
        index_names = cluster.index_names
        self.assertTrue(index_name in index_names)
        index.delete()

    def test_get_health(self):
        client = self._get_client()
        self.assertIsInstance(client.cluster.health, pylastica.cluster.health.Health)
