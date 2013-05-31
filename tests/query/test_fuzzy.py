__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class FuzzyTest(unittest.TestCase, Base):
    def test_query(self):
        index = self._create_index('test')
        doc_type = index.get_doc_type('test')
        doc_type.add_document(pylastica.Document(1, {'name': 'San Diego'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'San Luis Obispo'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'San Francisco'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'Chicago'}))
        index.refresh()

        query = pylastica.query.Fuzzy('name', 'San')
        result_set = doc_type.search(query)
        self.assertEqual(3, len(result_set))
        index.delete()

if __name__ == '__main__':
    unittest.main()
