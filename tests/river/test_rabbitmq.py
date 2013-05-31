__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class MyTestCase(unittest.TestCase, Base):
    def test_to_dict(self):
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
