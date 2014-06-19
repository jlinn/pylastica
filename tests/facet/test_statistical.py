__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class StatisticalTest(unittest.TestCase, Base):
    def test_statistical_with_set_field(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')

        doc_type.add_document(pylastica.Document(1, {'price': 10}))
        doc_type.add_document(pylastica.Document(2, {'price': 35}))
        doc_type.add_document(pylastica.Document(3, {'price': 45}))

        index.refresh()
        facet = pylastica.facet.Statistical('stats')
        facet.set_field('price')
        query = pylastica.query.Query()
        query.add_facet(facet)
        response = doc_type.search(query)
        facets = response.get_facets()
        self.assertEqual(90.0, facets['stats']['total'])
        self.assertEqual(10.0, facets['stats']['min'])
        self.assertEqual(45.0, facets['stats']['max'])
        index.delete()

    def test_statistical_with_set_fields(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')

        doc_type.add_document(pylastica.Document(1, {'price': 10, 'price2': 20}))
        doc_type.add_document(pylastica.Document(2, {'price': 35, 'price2': 70}))
        doc_type.add_document(pylastica.Document(2, {'price': 45, 'price2': 90}))

        index.refresh()
        facet = pylastica.facet.Statistical('stats')
        facet.set_fields(['price', 'price2'])
        query = pylastica.query.Query()
        query.add_facet(facet)
        response = doc_type.search(query)
        facets = response.get_facets()
        self.assertEqual(165, facets['stats']['total'])
        self.assertEqual(10, facets['stats']['min'])
        self.assertEqual(90, facets['stats']['max'])
        index.delete()

    def test_statistical_with_set_script(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')
        doc_type.add_document(pylastica.Document(1, {'price': 10}))
        doc_type.add_document(pylastica.Document(2, {'price': 35}))
        doc_type.add_document(pylastica.Document(3, {'price': 45}))

        index.refresh()
        facet = pylastica.facet.Statistical('stats')
        script = pylastica.Script("doc['price'].value + offset;", {'offset': 5})
        facet.set_script(script)
        query = pylastica.query.Query()
        query.add_facet(facet)
        response = doc_type.search(query)
        facets = response.get_facets()
        self.assertEqual(105.0, facets['stats']['total'])
        self.assertEqual(15.0, facets['stats']['min'])
        self.assertEqual(50.0, facets['stats']['max'])
        index.delete()

if __name__ == '__main__':
    unittest.main()
