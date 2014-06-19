__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class ExistsTest(unittest.TestCase, Base):
    def test_to_dict(self):
        field = 'test'
        exists_filter = pylastica.filter.Exists(field)
        expected = {
            'exists': {
                'field': field
            }
        }
        self.assertEqual(expected, exists_filter.to_dict())


if __name__ == '__main__':
    unittest.main()
