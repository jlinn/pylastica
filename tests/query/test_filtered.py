__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class FilteredTest(unittest.TestCase, Base):
    def test_filtered(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')

        doc_type.add_document(pylastica.Document(1, {'id': 1, 'email': 'test@test.com', 'username': 'bobloblaw', 'test': ['2', '3', '5']}))
        doc_type.add_document(pylastica.Document(2, {'id': 2, 'email': 'test@test.com', 'username': 'frank', 'test': ['2', '3', '5']}))
        index.refresh()

        query_string = pylastica.query.QueryString('test*')
        filter1 = pylastica.filter.Term().set_term('username', 'frank')
        filter2 = pylastica.filter.Term().set_term('username', 'asdfasedf')

        query1 = pylastica.query.Filtered(query_string, filter1)
        query2 = pylastica.query.Filtered(query_string, filter2)

        result_set = doc_type.search(query_string)
        self.assertEqual(2, len(result_set))

        result_set = doc_type.search(query1)
        self.assertEqual(1, len(result_set))

        result_set = doc_type.search(query2)
        self.assertEqual(0, len(result_set))
        index.delete()

if __name__ == '__main__':
    unittest.main()
