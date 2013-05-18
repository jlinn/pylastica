__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class BaseTest(unittest.TestCase, Base):
    def test_customscore(self):
        query = pylastica.query.MatchAll()
        customscore_query = pylastica.query.Cu


if __name__ == '__main__':
    unittest.main()
