__author__ = 'Joe Linn'

import unittest
import pylastica
from .base import *


class PercolatorTest(unittest.TestCase, Base):
    def setUp(self):
        self._index = self._create_index('test')

    def tearDown(self):
        self._index.delete()

    def test_match_doc(self):
        client = self._get_client()
        percolator = pylastica.Percolator(self._index)
        percolator_name = 'percotest'
        percolator_second_name = 'percotest_color'

        query = pylastica.query.Term({'name': 'linn'})
        response = percolator.register_query(percolator_name, query)
        self.assertTrue(response.is_ok())
        self.assertFalse(response.has_error())

        second_param_key = 'color'
        second_param_value = 'blue'
        query_second = pylastica.query.Query()
        query_second.query = query
        query_second.set_param(second_param_key, second_param_value)
        response_second = percolator.register_query(percolator_second_name, query_second)

        self.assertTrue(response_second.is_ok())
        self.assertFalse(response_second.has_error())

        doc1 = pylastica.Document().set('name', 'linn')
        doc2 = pylastica.Document().set('name', 'joe')

        index = pylastica.index.Index(client, '_percolator')
        index.optimize()
        index.refresh()

        matches1 = percolator.match_doc(doc1)

        self.assertTrue(percolator_name in matches1)
        self.assertTrue(percolator_second_name in matches1)
        self.assertEqual(2, len(matches1))

        matches2 = percolator.match_doc(doc2)
        self.assertEqual(0, len(matches2))

        doc_second = doc1
        doc_second.set(second_param_key, second_param_value)

        second_term = pylastica.query.Term({second_param_key: second_param_value})
        second_query = pylastica.query.Query()
        second_query.query = second_term

        second_matches = percolator.match_doc(doc_second, second_query)

        self.assertFalse(percolator_name in second_matches)
        self.assertTrue(percolator_second_name in second_matches)
        self.assertEqual(1, len(second_matches))


if __name__ == '__main__':
    unittest.main()
