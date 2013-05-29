__author__ = 'Joe Linn'

import unittest
import pylastica


class TermTest(unittest.TestCase):
    def test_to_dict(self):
        term_filter = pylastica.filter.Term()
        key = 'name'
        value = 'Linn'
        term_filter.set_term(key, value)
        data = term_filter.to_dict()
        self.assertEqual({key: value}, data['term'])


if __name__ == '__main__':
    unittest.main()
