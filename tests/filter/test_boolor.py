__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class BoolOrTest(unittest.TestCase, Base):
    def test_to_dict(self):
        or_filter = pylastica.filter.BoolOr()
        filter1 = pylastica.filter.Ids('1')
        filter2 = pylastica.filter.Ids('2')
        or_filter.add_filter(filter1).add_filter(filter2)
        expected_dict = {
            'or': {
                'filters': [
                    filter1.to_dict(),
                    filter2.to_dict()
                ]
            }
        }
        self.assertEqual(expected_dict, or_filter.to_dict())


if __name__ == '__main__':
    unittest.main()
