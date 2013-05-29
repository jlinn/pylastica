__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class DocTypeTest(unittest.TestCase, Base):
    def test_search(self):
        index = self._create_index()
        doc_type = index.get_doc_type('user')
        doc_type.add_document(pylastica.Document(1, {'username': 'bob', 'test': ['2', '3', '5']}))
        docs = [
            pylastica.Document(2, {'username': 'john', 'test': ['1', '3', '6']}),
            pylastica.Document(3, {'username': 'logan', 'test': ['2', '3', '7']})
        ]
        doc_type.add_documents(docs)
        index.refresh()

        result_set = doc_type.search('logan')
        self.assertEqual(1, len(result_set))

        self.assertEqual(1, doc_type.count('logan'))

        result = result_set[0]
        self.assertEqual('3', result.get_id())
        self.assertEqual('logan', result.data['username'])
        index.delete()


if __name__ == '__main__':
    unittest.main()
