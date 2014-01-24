__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class InfoTest(unittest.TestCase, Base):
    def test_get(self):
        client = self._get_client()
        names = client.cluster.node_names
        name = names[0]
        node = pylastica.node.Node(name, client)
        info = pylastica.node.Info(node)
        self.assertIsNone(info.get('os', 'mem', 'total'))

        info = pylastica.node.Info(node, ['os'])
        self.assertIsInstance(info.get('os', 'mem', 'total_in_bytes'), int)
        self.assertIsInstance(info.get('os', 'mem'), dict)
        self.assertIsNone(info.get('test', 'notest', 'notexist'))

    def test_has_plugin(self):
        client = self._get_client()
        names = client.cluster.node_names
        name = names[0]
        node = pylastica.node.Node(name, client)
        info = node.info

        plugin_name = 'mapper-attachments'
        self.assertTrue(info.has_plugin(plugin_name))
        self.assertFalse(info.has_plugin('foo'))

if __name__ == '__main__':
    unittest.main()
