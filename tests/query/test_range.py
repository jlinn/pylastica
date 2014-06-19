__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class RangeTest(unittest.TestCase, Base):
    def test_query(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('test')

        doc_type.add_document(pylastica.Document(1, {'age': 16, 'height': 140}))
        doc_type.add_document(pylastica.Document(2, {'age': 21, 'height': 155}))
        doc_type.add_document(pylastica.Document(3, {'age': 33, 'height': 160}))
        doc_type.add_document(pylastica.Document(4, {'age': 68, 'height': 160}))

        index.optimize()
        index.refresh()

        query = pylastica.query.Range('age', {'from': 10, 'to': 20})
        result = doc_type.search(query)
        self.assertEqual(1, len(result))

        query = pylastica.query.Range('height', {'gte': 160})
        result = doc_type.search(query)
        self.assertEqual(2, len(result))
        index.delete()


if __name__ == '__main__':
    unittest.main()
