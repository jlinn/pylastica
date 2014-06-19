__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class BaseTest(unittest.TestCase, Base):
    def test_customscore(self):
        query = pylastica.query.MatchAll()
        customscore_query = pylastica.query.CustomScore()


if __name__ == '__main__':
    unittest.main()
