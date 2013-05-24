__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class WildcardTest(unittest.TestCase, Base):
    def test_search_with_analyzer(self):
        client = self._get_client()
        index = client.get_index('test')
        index_params = {
            'analysis': {
                'analyzer': {
                    'lw': {
                        'type': 'custom',
                        'tokenizer': 'keyword',
                        'filter': ['lowercase']
                    }
                }
            }
        }
        index.create(index_params, True)
        doc_type = index.get_doc_type('test')
        mapping = pylastica.doc_type.Mapping(doc_type, {
            'name': {'type': 'string', 'store': 'no', 'analyzer': 'la'}
        })
        doc_type.mapping = mapping

        doc_type.add_document(pylastica.Document(1, {'name': 'San Diego'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'San Luis Obispo'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'San Francisco'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'Chicago'}))
        doc_type.add_document(pylastica.Document(5, {'name': 'London'}))
        index.refresh()

        query = pylastica.query.Wildcard()
        query.set_value('name', 'sa*')
        result_set = doc_type.search(query)
        self.assertEqual(3, len(result_set))

        query = pylastica.query.Wildcard()
        query.set_value('name', 'ch*')
        result_set = doc_type.search(query)
        self.assertEqual(1, len(result_set))
        index.delete()


if __name__ == '__main__':
    unittest.main()
