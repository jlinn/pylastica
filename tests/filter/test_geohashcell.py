__author__ = 'Joe Linn'

import unittest
from tests.base import Base
import pylastica


class GeohashCellTest(unittest.TestCase, Base):
    def test_to_dict(self):
        geohash_cell_filter = pylastica.filter.GeohashCell('pin', {'lat': 37.789018, 'lon': -122.391506}, '50m')
        expected = {
            'geohash_cell': {
                'pin': {
                    'lat': 37.789018,
                    'lon': -122.391506
                },
                'precision': '50m',
                'neighbors': False
            }
        }
        self.assertEqual(geohash_cell_filter.to_dict(), expected)

    def test_filter(self):
        index = self._create_index('geohash_filter_test')
        doc_type = index.get_doc_type('test')
        mapping = pylastica.doc_type.Mapping(doc_type, {
            'pin': {
                'type': 'geo_point',
                'geohash': True,
                'geohash_prefix': True
            }
        })
        doc_type.mapping = mapping

        doc_type.add_document(pylastica.Document(1, {'pin': '9q8yyzm0zpw8'}))
        doc_type.add_document(pylastica.Document(2, {'pin': '9mudgb0yued0'}))
        index.refresh()

        geohash_cell_filter = pylastica.filter.GeohashCell('pin', {'lat': 32.828326, 'lon': -117.255854})
        query = pylastica.query.Query().set_filter(geohash_cell_filter)
        results = doc_type.search(query)

        self.assertEqual(1, len(results.results))

        geohash_cell_filter = pylastica.filter.GeohashCell('pin', '9', 1)
        query = pylastica.query.Query().set_filter(geohash_cell_filter)
        results = doc_type.search(query)

        self.assertEqual(2, len(results.results))

        index.delete()


if __name__ == '__main__':
    unittest.main()
