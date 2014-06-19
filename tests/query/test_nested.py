__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class NestedTest(unittest.TestCase, Base):
    def test_set_query(self):
        nested = pylastica.query.Nested()
        path = 'test1'
        query_string = pylastica.query.QueryString('test')
        self.assertIsInstance(nested.set_query(query_string), pylastica.query.Nested)
        self.assertIsInstance(nested.set_path(path), pylastica.query.Nested)
        expected = {
            'nested': {
                'query': query_string.to_dict(),
                'path': path
            }
        }
        self.assertEqual(expected, nested.to_dict())


if __name__ == '__main__':
    unittest.main()
