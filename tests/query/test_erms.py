__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class TermsTest(unittest.TestCase, Base):
    def test_filtered_search(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')
        doc_type.add_document(pylastica.Document(1, {'name': 'hello world'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'Joe Linn'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'Linn'}))
        index.refresh()

        query = pylastica.query.Terms()
        query.set_terms('name', ['joe', 'hello'])
        result_set = doc_type.search(query)
        self.assertEqual(2, len(result_set))

        query.add_term('linn')
        result_set = doc_type.search(query)
        self.assertEqual(3, len(result_set))

        index.delete()


if __name__ == '__main__':
    unittest.main()
