__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class MyTestCase(unittest.TestCase, Base):
    def setUp(self):
        client = self._get_client()
        node = client.cluster.nodes[0]
        self._has_rabbit_river = node.info.has_plugin('river-rabbitmq')

    def test_to_dict(self):
        if not self._has_rabbit_river:
            self.skipTest('The river-rabbitmq plugin is not installed.')
        client = self._get_client()
        river = pylastica.river.RabbitMQ(client, 'test_river', index='test')
        expected = {
            'type': 'rabbitmq',
            'rabbitmq': {
                'host': 'localhost',
                'port': 5672,
                'user': 'guest',
                'pass': 'guest'
            },
            'index': {
                'name': 'test',
                'bulk_timeout': '10ms',
                'bulk_size': 100
            }
        }
        self.assertEqual(expected, river.to_dict())

    def test_create_and_delete(self):
        if not self._has_rabbit_river:
            self.skipTest('The river-rabbitmq plugin is not installed.')
        client = self._get_client()
        river = pylastica.river.RabbitMQ(client, 'test_river')
        response = river.create()
        self.assertTrue(response.is_ok())
        self.assertFalse(response.has_error())
        response = river.delete()
        self.assertTrue(response.is_ok())
        self.assertFalse(response.has_error())


if __name__ == '__main__':
    unittest.main()
