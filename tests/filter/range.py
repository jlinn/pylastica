__author__ = 'Joe Linn'

import unittest
import pylastica


class RangeTest(unittest.TestCase):
    def test_to_dict(self):
        range_filter = pylastica.filter.Range()
        from_to = {'from': 'ra', 'to': 'ru'}
        range_filter.add_field('name', from_to)
        expected = {
            'range': {
                'name': from_to
            }
        }
        self.assertEqual(expected, range_filter.to_dict())


if __name__ == '__main__':
    unittest.main()
