__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class TextTest(unittest.TestCase, Base):
    def test_text_phrase(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('test')

        doc_type.add_document(pylastica.Document(1, {'name': 'San Diego'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'San Luis Obispo'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'San Francisco'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'Chicago'}))
        index.refresh()

        field_type = 'text_phrase'
        field = 'name'
        query = pylastica.query.Text()
        query.set_field_query(field, 'San')
        query.set_field('operator', 'OR')
        query.set_field_type(field, field_type)
        result_set = index.search(query)
        self.assertEqual(2, len(result_set))
        index.delete()

if __name__ == '__main__':
    unittest.main()
