__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class QueryTest(unittest.TestCase, Base):
    def test_query(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')
        doc_type.add_document(pylastica.Document(1, {'color': 'red'}))
        doc_type.add_document(pylastica.Document(2, {'color': 'green'}))
        doc_type.add_document(pylastica.Document(3, {'color': 'blue'}))
        index.refresh()
        term_query = pylastica.query.Term({'color': 'red'})
        facet = pylastica.facet.Query('test')
        facet.set_query(term_query)
        query = pylastica.query.Query()
        query.add_facet(facet)
        result_set = doc_type.search(query)
        facets = result_set.get_facets()
        self.assertEqual(1, facets['test']['count'])
        index.delete()


if __name__ == '__main__':
    unittest.main()
