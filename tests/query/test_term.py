__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class TermTest(unittest.TestCase, Base):
    def test_to_dict(self):
        query = pylastica.query.Term()
        key = 'name'
        value = 'Joe'
        boost = 2
        query.set_term(key, value, boost)
        data = query.to_dict()
        self.assertIsInstance(data['term'], dict)
        self.assertIsInstance(data['term'][key], dict)
        self.assertEqual(data['term'][key]['value'], value)
        self.assertEqual(data['term'][key]['boost'], boost)


if __name__ == '__main__':
    unittest.main()
