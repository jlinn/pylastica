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

        self._index.refresh()

        matches1 = percolator.match_doc(doc1)

        first_percolator_found = False
        second_percolator_found = False
        for match in matches1:
            if match['_id'] == percolator_name:
                first_percolator_found = True
            if match['_id'] == percolator_second_name:
                second_percolator_found = True
        self.assertTrue(first_percolator_found)
        self.assertTrue(second_percolator_found)
        self.assertEqual(2, len(matches1))

        matches2 = percolator.match_doc(doc2)
        self.assertEqual(0, len(matches2))

        doc_second = doc1
        doc_second.set(second_param_key, second_param_value)

        second_term = pylastica.query.Term({second_param_key: second_param_value})
        second_query = pylastica.query.Query()
        second_query.query = second_term

        second_matches = percolator.match_doc(doc_second, second_query)

        first_percolator_found = False
        second_percolator_found = False
        for match in second_matches:
            if match['_id'] == percolator_name:
                first_percolator_found = True
            if match['_id'] == percolator_second_name:
                second_percolator_found = True
        self.assertFalse(first_percolator_found)
        self.assertTrue(second_percolator_found)
        self.assertEqual(1, len(second_matches))


if __name__ == '__main__':
    unittest.main()
