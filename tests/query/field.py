__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class FieldTest(unittest.TestCase, Base):
    def test_text_phrase(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('test')

        doc_type.add_document(pylastica.Document(1, {'name': 'San Diego'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'San Luis Obispo'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'Chicago'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'San Francisco'}))

        index.refresh()
        query = pylastica.query.Field()
        query.set_field('name')
        query.set_query_string('Diego')
        result_set = index.search(query)
        self.assertEqual(1, len(result_set))
        index.delete()


if __name__ == '__main__':
    unittest.main()
