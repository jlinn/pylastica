__author__ = 'Joe Linn'

import unittest
import pylastica


class MatchAllTest(unittest.TestCase):
    def test_to_dict(self):
        match_all = pylastica.filter.MatchAll()
        expected = {
            'match_all': {}
        }
        self.assertEqual(expected, match_all.to_dict())


if __name__ == '__main__':
    unittest.main()
