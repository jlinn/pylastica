__author__ = 'Joe Linn'

import unittest
import pylastica
from .base import *


class StatusTest(unittest.TestCase, Base):
    def test_get_response(self):
        index = self._create_index()
        status = pylastica.Status(index.client)
        self.assertIsInstance(status.response, pylastica.Response)
        index.delete()

    def test_get_index_statuses(self):
        index = self._create_index()
        status = pylastica.Status(index.client)
        statuses = status.index_statuses

        self.assertIsInstance(statuses, list)

        for index_status in statuses:
            self.assertIsInstance(index_status, pylastica.index.Status)

        index.delete()

    def test_get_index_names(self):
        index_name = 'test'
        client = self._get_client()
        index = client.get_index(index_name)
        index.create(options=True)
        status = pylastica.Status(client)
        names = status.index_names

        self.assertIsInstance(names, list)
        self.assertTrue(index.name in names)

        for name in names:
            self.assertIsInstance(name, unicode)
        index.delete()

    def test_index_exists(self):
        index_name = 'pylastica_test'
        client = self._get_client()
        index = client.get_index(index_name)
        try:
            index.delete()
        except pylastica.exception.ResponseException as e:
            pass

        status = pylastica.Status(client)

        self.assertFalse(status.index_exists(index_name))

        index.create()
        status.refresh()

        self.assertTrue(status.index_exists(index_name))
        index.delete()

    def test_alias_exists(self):
        alias_name = 'pylastica_test-alias'
        index = self._create_index()
        status = pylastica.Status(index.client)

        for tmp_index in status.get_indices_with_alias(alias_name):
            tmp_index.remove_alias(alias_name)

        self.assertFalse(status.alias_exists(alias_name))

        index.add_alias(alias_name)
        status.refresh()

        self.assertTrue(status.alias_exists(alias_name))
        index.delete()

    def test_server_status(self):
        status = self._get_client().status
        server_status = status.server_status

        self.assertIsInstance(server_status, dict)
        self.assertTrue('ok' in server_status)
        self.assertTrue(server_status['ok'])
        self.assertTrue('version' in server_status)

        version_info = server_status['version']
        self.assertTrue('number' in version_info)

    def test_get_indices_with_alias(self):
        index_name1 = 'test1'
        index_name2 = 'test2'
        alias_name = 'test-alias'
        client = self._get_client()
        index1 = pylastica.index.Index(client, index_name1)
        index1.create(options=True)
        index2 = pylastica.index.Index(client, index_name2)
        index2.create(options=True)
        index1.add_alias(alias_name)
        index2.add_alias(alias_name)

        status = client.status
        indices = status.get_indices_with_alias(alias_name)

        self.assertEqual(indices[0].name, index1.name)
        self.assertEqual(indices[1].name, index2.name)

        index1.delete()
        index2.delete()


if __name__ == '__main__':
    unittest.main()
