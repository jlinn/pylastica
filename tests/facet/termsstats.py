__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class TermsStatsTest(unittest.TestCase, Base):
    def test_termsstats(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')

        doc_type.add_document(pylastica.Document(1, {'name': 'tom', 'paid': 7}))
        doc_type.add_document(pylastica.Document(2, {'name': 'tom', 'paid': 2}))
        doc_type.add_document(pylastica.Document(3, {'name': 'tom', 'paid': 5}))
        doc_type.add_document(pylastica.Document(4, {'name': 'mike', 'paid': 13}))
        doc_type.add_document(pylastica.Document(5, {'name': 'mike', 'paid': 1}))
        doc_type.add_document(pylastica.Document(6, {'name': 'mike', 'paid': 15}))

        index.refresh()
        facet = pylastica.facet.TermsStats('test')
        facet.set_key_field('name')
        facet.set_value_field('paid')
        query = pylastica.query.Query()
        query.add_facet(facet)
        response = doc_type.search(query)
        facets = response.get_facets()
        self.assertEqual(2, len(facets['test']['terms']))
        for facet in facets['test']['terms']:
            if facet['term'] == 'tom':
                self.assertEqual(14, facet['total'])
            elif facet['term'] == 'mike':
                self.assertEqual(29, facet['total'])
        index.delete()


if __name__ == '__main__':
    unittest.main()
