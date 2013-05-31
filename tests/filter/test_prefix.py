__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class PrefixTest(unittest.TestCase, Base):
    def test_different_prefixes(self):
        index = self._create_index('test')
        doc_type = index.get_doc_type('test')
        mapping = pylastica.doc_type.Mapping(doc_type, {
            'name': {'type': 'string', 'store': 'no', 'index': 'not_analyzed'}
        })
        doc_type.mapping = mapping

        doc_type.add_document(pylastica.Document(1, {'name': 'San Diego'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'San Luis Obispo'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'San Francisco'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'New Orleans'}))
        doc_type.add_document(pylastica.Document(5, {'name': 'New York'}))

        index.refresh()

        query = pylastica.filter.Prefix('name', 'Sa')
        self.assertEqual(3, len(doc_type.search(query)))

        query = pylastica.filter.Prefix('name', 'sa')
        self.assertEqual(0, len(doc_type.search(query)))

        query = pylastica.filter.Prefix('name', 'San D')
        self.assertEqual(1, len(doc_type.search(query)))

        query = pylastica.filter.Prefix('name', 'San Db')
        self.assertEqual(0, len(doc_type.search(query)))
        index.delete()

    def test_different_prefixes_lowercase(self):
        index = self._create_index('test')
        doc_type = index.get_doc_type('test')
        mapping = pylastica.doc_type.Mapping(doc_type, {
            'name': {'type': 'string', 'store': 'no', 'analyzer': 'lw'}
        })
        doc_type.mapping = mapping

        doc_type.add_document(pylastica.Document(1, {'name': 'San Diego'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'San Luis Obispo'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'San Francisco'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'New Orleans'}))
        doc_type.add_document(pylastica.Document(5, {'name': 'New York'}))

        index.refresh()

        query = pylastica.filter.Prefix('name', 'sa')
        self.assertEqual(3, len(doc_type.search(query)))

        query = pylastica.filter.Prefix('name', 'Sa')
        self.assertEqual(0, len(doc_type.search(query)))

        index.delete()


if __name__ == '__main__':
    unittest.main()
