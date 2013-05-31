__author__ = 'Joe Linn'

import unittest
import pylastica


class ScriptTest(unittest.TestCase):
    def test_to_dict(self):
        string = '_score * 2.0'
        script_filter = pylastica.filter.Script(string)
        dictionary = script_filter.to_dict()
        self.assertIsInstance(dictionary, dict)

        expected = {
            'script': {
                'script': string
            }
        }
        self.assertEqual(expected, dictionary)


if __name__ == '__main__':
    unittest.main()
