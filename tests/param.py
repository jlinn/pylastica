__author__ = 'Joe Linn'

import unittest
import pylastica.param

class ParamTestCase(unittest.TestCase):
    def test_param(self):
        param = pylastica.param.Param()
        param.params = {'test': 'param!'}
        self.assertIsInstance(param.to_dict(), dict)
        self.assertIn('param', param.to_dict())

if __name__ == '__main__':
    unittest.main()
