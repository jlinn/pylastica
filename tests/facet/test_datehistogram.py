__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class DateHistogramTest(unittest.TestCase, Base):
    def test_facet(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworld')
        mapping = pylastica.doc_type.Mapping(doc_type, {
            'name': {'type': 'string', 'store': 'no'},
            'dtmPosted': {'type': 'date', 'store': 'no', 'format': 'yyyy-MM-dd HH:mm:ss'}
        })
        doc_type.mapping = mapping

        doc_type.add_document(pylastica.Document(1, {'name': 'Joe Linn', 'dtmPosted': '2013-05-17 03:44:00'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'Sterling Archer', 'dtmPosted': '2013-04-17 00:14:00'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'Cyril Figgis', 'dtmPosted': '2013-05-17 10:54:00'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'Lana Kane', 'dtmPosted': '2013-01-02 18:37:00'}))
        index.refresh()

        facet = pylastica.facet.DateHistogram('dateHist1')
        facet.set_interval('day')
        facet.set_field('dtmPosted')

        query = pylastica.query.Query()
        query.add_facet(facet)
        response = doc_type.search(query)
        facets = response.get_facets()
        self.assertEqual(4, response.get_total_hits())
        self.assertEqual(3, len(facets['dateHist1']['entries']))
        index.delete()

if __name__ == '__main__':
    unittest.main()
