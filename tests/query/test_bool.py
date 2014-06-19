__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class BoolTest(unittest.TestCase, Base):
    def test_search(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')

        doc_type.add_document(pylastica.Document(1, {'id': 1, 'email': 'joe@test.com', 'username': 'joe', 'test': ['2', '3', '5']}))
        doc_type.add_document(pylastica.Document(2, {'id': 2, 'email': 'bob@test.com', 'username': 'bob', 'test': ['1', '3', '6']}))
        doc_type.add_document(pylastica.Document(3, {'id': 3, 'email': 'bill@test.com', 'username': 'bill', 'test': ['2', '3', '7']}))

        index.refresh()
        bool_query = pylastica.query.Bool()
        term_query1 = pylastica.query.Term({'test': '2'})
        bool_query.add_must(term_query1)
        result_set = doc_type.search(bool_query)

        self.assertEqual(2, len(result_set))

        term_query2 = pylastica.query.Term({'test': '5'})
        bool_query.add_must(term_query2)
        result_set = doc_type.search(bool_query)

        self.assertEqual(1, len(result_set))

        term_query3 = pylastica.query.Term({'username': 'joe'})
        bool_query.add_must(term_query3)
        result_set = doc_type.search(bool_query)

        self.assertEqual(1, len(result_set))

        term_query4 = pylastica.query.Term({'username': 'bob'})
        bool_query.add_must(term_query4)
        result_set = doc_type.search(bool_query)

        self.assertEqual(0, len(result_set))
        index.delete()


if __name__ == '__main__':
    unittest.main()
