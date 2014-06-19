__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class PrefixTest(unittest.TestCase, Base):
    def test_to_dict(self):
        query = pylastica.query.Prefix()
        key = 'name'
        value = 'ni'
        boost = 2
        query.set_prefix(key, value, boost)
        data = query.to_dict()
        self.assertIsInstance(data['prefix'], dict)
        self.assertIsInstance(data['prefix'][key], dict)
        self.assertEqual(data['prefix'][key]['value'], value)
        self.assertEqual(data['prefix'][key]['boost'], boost)


if __name__ == '__main__':
    unittest.main()
