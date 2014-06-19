__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class GeoDistanceRangeTest(unittest.TestCase, Base):
    def test_geo_point(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('test')
        doc_type.mapping = {
            'point': {'type': 'geo_point'}
        }
        doc_type.add_document(pylastica.Document(1, {'name': 'Linn'}).add_geopoint('point', 17, 19))
        doc_type.add_document(pylastica.Document(2, {'name': 'Linn'}).add_geopoint('point', 30, 40))
        index.optimize()
        index.refresh()
        query = pylastica.query.Query()
        geo_filter = pylastica.filter.GeoDistanceRange('point', {'lat': 30, 'lon': 40}, upper='2km', lower='0km')
        query.set_filter(geo_filter)
        self.assertEqual(1, len(doc_type.search(query)))

        query = pylastica.query.Query()
        geo_filter = pylastica.filter.GeoDistanceRange('point', {'lat': 30, 'lon': 40}, lower='0km', upper='40000km')
        query.set_filter(geo_filter)
        index.refresh()
        self.assertEqual(2, len(doc_type.search(query)))
        index.delete()


if __name__ == '__main__':
    unittest.main()
