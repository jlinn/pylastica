__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class TextTest(unittest.TestCase, Base):
    def test_to_dict(self):
        query_text = 'Joe Linn'
        query_type = 'text_phrase'
        analyzer = 'myanalyzer'
        max_expansions = 12
        field = 'test'

        query = pylastica.query.Text()
        query.set_field_query(field, query_text)
        query. set_field_type(field, query_type)
        query.set_field_param(field, 'analyzer', analyzer)
        query.set_field_max_expansions(field, max_expansions)

        expected = {
            'text': {
                field: {
                    'query': query_text,
                    'type': query_type,
                    'analyzer': analyzer,
                    'max_expansions': max_expansions
                }
            }
        }
        self.assertEqual(expected, query.to_dict())

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
        query.set_field_query(field, 'Chicago San')
        query.set_field_param(field, 'operator', 'or')
        query.set_field_type(field, field_type)
        result_set = index.search(query)
        print result_set.response.error
        self.assertEqual(4, len(result_set))
        index.delete()

if __name__ == '__main__':
    unittest.main()
