__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class SettingsTest(unittest.TestCase, Base):
    def test_set_transient(self):
        index = self._create_index()
        if len(index.client.cluster.nodes) < 2:
            self.skipTest("At least two master nodes must be running for this test.")
        settings = pylastica.cluster.Settings(index.client)
        settings.set_transient('discovery.zen.minimum_master_nodes', 2)
        data = settings.get()
        self.assertEqual(2, int(data['transient']['discovery.zen.minimum_master_nodes']))
        index.delete()


if __name__ == '__main__':
    unittest.main()
