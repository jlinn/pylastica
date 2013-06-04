__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class StatusTest(unittest.TestCase, Base):
    def test_get_aliases(self):
        index_name = 'test'
        alias_name = 'test-alias'
        index = self._create_index(index_name)
        status = pylastica.index.Status(index)

        aliases = status.aliases
        self.assertEqual(0, len(aliases))

        index.add_alias(alias_name)
        status.refresh()

        aliases = status.aliases
        self.assertTrue(alias_name in aliases)

        index.delete()

    def test_has_alias(self):
        index_name = 'test'
        alias_name = 'test-alias'
        index = self._create_index(index_name)
        status = pylastica.index.Status(index)

        self.assertFalse(status.has_alias(alias_name))

        index.add_alias(alias_name)
        status.refresh()

        self.assertTrue(status.has_alias(alias_name))

        index.delete()

    def test_get_settings(self):
        index_name = 'test'
        index = self._create_index(index_name)
        status = index.status
        settings = status.settings

        self.assertIsInstance(settings, dict)
        self.assertTrue('index.number_of_shards' in settings)
        index.delete()


if __name__ == '__main__':
    unittest.main()
