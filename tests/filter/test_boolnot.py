__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class BoolNotTest(unittest.TestCase, Base):
    def test_to_array(self):
        ids_filter = pylastica.filter.Ids('12')
        bool_filter = pylastica.filter.BoolNot(ids_filter)
        expected_dict = {
            'not': {
                'filter': ids_filter.to_dict()
            }
        }
        self.assertEqual(expected_dict, bool_filter.to_dict())

if __name__ == '__main__':
    unittest.main()
