__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class HasParentTest(unittest.TestCase, Base):
    def test_to_dict(self):
        q = pylastica.query.MatchAll()
        doc_type = 'test'
        query = pylastica.query.HasParent(q, doc_type)
        expected = {
            'has_parent': {
                'query': q.to_dict(),
                'type': doc_type
            }
        }
        self.assertEqual(expected, query.to_dict())


if __name__ == '__main__':
    unittest.main()
