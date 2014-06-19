__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class GeoPolygonTest(unittest.TestCase, Base):
    def test_geo_point(self):
        index = self._create_index('test')
        doc_type = index.get_doc_type('test')
        doc_type.mapping = {
            'point': {
                'type': 'geo_point'
            }
        }
        doc_type.add_document(pylastica.Document(1, {'name': 'Linn'}).add_geopoint('point', 17, 19))
        doc_type.add_document(pylastica.Document(2, {'name': 'Linn'}).add_geopoint('point', 30, 40))
        index.refresh()
        query = pylastica.query.Query()
        points = [
            [16, 16],
            [16, 20],
            [20, 20],
            [20, 16],
            [16, 16]
        ]
        geo_filter = pylastica.filter.GeoPolygon('point', points)
        query.set_filter(geo_filter)
        self.assertEqual(1, len(doc_type.search(query)))

        query = pylastica.query.Query()
        points = [
            [16, 16],
            [16, 40],
            [40, 40],
            [40, 16],
            [16, 16]
        ]
        geo_filter = pylastica.filter.GeoPolygon('point', points)
        query.set_filter(geo_filter)
        self.assertEqual(2, len(doc_type.search(query)))
        index.delete()


if __name__ == '__main__':
    unittest.main()
