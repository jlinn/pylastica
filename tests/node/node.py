__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class NodeTest(unittest.TestCase, Base):
    def test_get_info(self):
        client = self._get_client()
        names = client.cluster.node_names
        name = names[0]
        node = pylastica.node.Node(name, client)
        info = node.info
        self.assertIsInstance(info, pylastica.node.Info)

    def test_get_stats(self):
        client = self._get_client()
        names = client.cluster.node_names
        name = names[0]
        node = pylastica.node.Node(name, client)
        stats = node.stats
        self.assertIsInstance(stats, pylastica.node.Stats)


if __name__ == '__main__':
    unittest.main()
