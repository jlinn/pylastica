__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class MatchTest(unittest.TestCase, Base):
    def setUp(self):
        index = self._create_index('test')
        doc_type = index.get_doc_type('test')
        doc_type.add_document(pylastica.Document(1, {'name': 'San Diego'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'San Luis Obispo'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'San Francisco'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'Chicago'}))
        index.refresh()
        self._index = index

    def tearDown(self):
        self._index.delete()

    def test_match(self):
        field = 'name'
        operator = 'or'
        query = pylastica.query.Match()
        query.set_field_query(field, 'San Chicago')
        query.set_field_operator(field, operator)
        result_set = self._index.search(query)
        self.assertEqual(4, len(result_set))

    def test_match_phrase(self):
        field = 'name'
        field_type = 'phrase'
        query = pylastica.query.Match()
        query.set_field_query(field, 'San Diego')
        query.set_field_type(field, field_type)
        result_set = self._index.search(query)
        self.assertEqual(1, len(result_set))

    def test_match_phrase_prefix(self):
        field = 'name'
        field_type = 'phrase_prefix'
        query = pylastica.query.Match()
        query.set_field_query(field, 'San')
        query.set_field_type(field, field_type)
        result_set = self._index.search(query)
        self.assertEqual(3, len(result_set))


if __name__ == '__main__':
    unittest.main()
