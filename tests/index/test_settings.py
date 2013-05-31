__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class SettingsTest(unittest.TestCase, Base):
    def test_get(self):
        index_name = 'pylasticatest'
        client = self._get_client()
        index = client.get_index(index_name)
        index.create(options=True)
        index.refresh()
        settings = index.settings
        self.assertIsNotNone(settings.get('number_of_replicas'))
        self.assertIsNotNone(settings.get('number_of_shards'))
        self.assertIsNone(settings.get('oiwefoawef'))
        index.delete()

    def test_set_number_of_replicas(self):
        index_name = 'test'
        client = self._get_client()
        index = client.get_index(index_name)
        index.create(options=True)
        settings = index.settings
        settings.set_number_of_replicas(0)
        index.refresh()
        self.assertEqual(0, int(settings.get('number_of_replicas')))
        index.delete()

    def test_set_refresh_interval(self):
        index_name = 'test'
        client = self._get_client()
        index = client.get_index(index_name)
        index.create(options=True)
        settings = index.settings
        settings.set_refresh_interval('2s')
        index.refresh()
        self.assertEqual('2s', settings.get('refresh_interval'))
        index.delete()

    def test_get_settings(self):
        index = self._create_index('test')
        settings = index.status.settings

        self.assertTrue('index.number_of_shards' in settings)
        index.delete()

if __name__ == '__main__':
    unittest.main()
