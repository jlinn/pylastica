__author__ = 'Joe Linn'

import unittest
import pylastica.util

class UtilTest(unittest.TestCase):
    def test_to_snake_case(self):
        result = pylastica.util.to_snake_case('TestString')
        self.assertEqual(result, 'test_string')

    def test_get_param_name(self):
        class GenericFilter(object):
            pass
        generic = GenericFilter()
        result = pylastica.util.get_param_name(generic)
        self.assertEqual(result, 'generic')

if __name__ == '__main__':
    unittest.main()
