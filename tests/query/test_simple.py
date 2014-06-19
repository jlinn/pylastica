__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class SimpleTest(unittest.TestCase, Base):
    def test_to_dict(self):
        test_query = {
            'hello': ['world'],
            'name': 'Linn'
        }
        query = pylastica.query.Simple(test_query)
        self.assertEqual(test_query, query.to_dict())


if __name__ == '__main__':
    unittest.main()
