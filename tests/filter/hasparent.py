__author__ = 'Joe Linn'

import unittest
import pylastica


class HasParentTest(unittest.TestCase):
    def test_to_dict(self):
        q = pylastica.query.MatchAll()
        doc_type = 'test'
        test_filter = pylastica.filter.HasParent(q, doc_type)
        expected = {
            'has_parent': {
                'query': q.to_dict(),
                'type': doc_type
            }
        }
        self.assertEqual(expected, test_filter.to_dict())


if __name__ == '__main__':
    unittest.main()
