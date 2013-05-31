__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class FilterTest(unittest.TestCase, Base):
    def test_filter(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')
        doc_type.add_document(pylastica.Document(1, {'color': 'red'}))
        doc_type.add_document(pylastica.Document(2, {'color': 'green'}))
        doc_type.add_document(pylastica.Document(3, {'color': 'blue'}))
        index.refresh()
        term_filter = pylastica.filter.Term('color', 'red')
        facet = pylastica.facet.Filter('test')
        facet.set_filter(term_filter)
        query = pylastica.query.Query()
        query.add_facet(facet)
        result_set = doc_type.search(query)
        facets = result_set.get_facets()
        self.assertEqual(1, facets['test']['count'])
        index.delete()

if __name__ == '__main__':
    unittest.main()
