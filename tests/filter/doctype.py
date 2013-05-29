__author__ = 'Joe Linn'

import unittest
import pylastica


class DocTypeTest(unittest.TestCase):
    def test_to_dict(self):
        type_filter = pylastica.filter.DocType('type_name')
        expected = {
            'type': {'value': 'type_name'}
        }
        self.assertEqual(expected, type_filter.to_dict())


if __name__ == '__main__':
    unittest.main()
