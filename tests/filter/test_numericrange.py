__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class NumericRangeTest(unittest.TestCase, Base):
    def test_to_dict(self):
        range_filter = pylastica.filter.NumericRange()
        from_to = {'from': 'ra', 'to': 'ru'}
        range_filter.add_field('name', from_to)
        expected = {
            'numeric_range': {
                'name': from_to
            }
        }
        self.assertEqual(expected, range_filter.to_dict())


if __name__ == '__main__':
    unittest.main()
