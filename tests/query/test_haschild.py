__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class HasChildTest(unittest.TestCase, Base):
    def test_to_array(self):
        q = pylastica.query.MatchAll()
        query = pylastica.query.HasChild(q, 'test')
        expected = {
            'has_child': {
                'query': q.to_dict(),
                'type': 'test'
            }
        }
        self.assertEqual(expected, query.to_dict())

    def test_set_scope(self):
        q = pylastica.query.MatchAll()
        doc_type = 'test'
        scope = 'foo'
        query = pylastica.query.HasChild(q, doc_type)
        query.set_scope(scope)
        expected = {
            'has_child': {
                'query': q.to_dict(),
                'type': doc_type,
                '_scope': scope
            }
        }
        self.assertEqual(expected, query.to_dict())


if __name__ == '__main__':
    unittest.main()
