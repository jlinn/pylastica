__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class TermsTest(unittest.TestCase, Base):
    def test_query(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')

        doc_type.add_document(pylastica.Document(1, {'name': 'Joe Linn'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'Derek Gould'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'Marc Hoag'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'Ryan Lum'}))

        index.refresh()
        facet = pylastica.facet.Terms('test')
        facet.set_field('name')
        query = pylastica.query.Query()
        query.add_facet(facet)
        response = doc_type.search(query)
        facets = response.get_facets()
        self.assertEqual(8, len(facets['test']['terms']))
        index.delete()

    def test_facet_script(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')

        doc_type.add_document(pylastica.Document(1, {'name': 'Tyler', 'last_name': 'Durden'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'Marla', 'last_name': 'Singer'}))

        index.refresh()
        facet = pylastica.facet.Terms('test')
        facet.set_field('name')
        facet.set_script(pylastica.Script('term + " " + doc["last_name"].value'))
        query = pylastica.query.Query()
        query.add_facet(facet)
        response = doc_type.search(query)
        facets = response.get_facets()
        self.assertEqual(2, len(facets['test']['terms']))
        index.delete()

    def test_facet_filter(self):
        index = self._create_index('test')
        doc_type = index.get_doc_type('test')

        doc_type.add_document(pylastica.Document(1, {'name': 'Michael', 'last_name': 'Bluth'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'George', 'last_name': 'Bluth'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'Buster', 'last_name': 'Bluth'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'Bob', 'last_name': 'Loblaw'}))
        index.refresh()

        facet = pylastica.facet.Terms('test')
        facet.set_field('name')
        facet.set_filter(pylastica.filter.Term('last_name', 'bluth'))
        query = pylastica.query.Query()
        query.add_facet(facet)
        response = doc_type.search(query)
        facets = response.get_facets()

        self.assertEqual(3, len(facets['test']['terms']))
        index.delete()


if __name__ == '__main__':
    unittest.main()
