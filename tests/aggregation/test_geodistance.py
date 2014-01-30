from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.geodistance import GeoDistance
from pylastica.doc_type import Mapping
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class GeoDistanceTest(unittest.TestCase, Base):
    def setUp(self):
        super(GeoDistanceTest, self).setUp()
        self._index = self._create_index("test_aggregation_geo_distance")
        mapping = Mapping()
        mapping.set_properties({
            "location": {"type": "geo_point"}
        })
        doc_type = self._index.get_doc_type("test")
        doc_type.mapping = mapping
        docs = [
            Document("1", {"location": {'lat': 32.849437, 'lon': -117.271732}}),
            Document("2", {"location": {'lat': 32.798320, 'lon': -117.246648}}),
            Document("3", {"location": {'lat': 37.782439, 'lon': -122.392560}}),
        ]
        doc_type.add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(GeoDistanceTest, self).tearDown()
        self._index.delete()

    def test_geo_distance_aggregation(self):
        agg = GeoDistance("geo", "location", {'lat': 32.804654, 'lon': -117.242594})
        agg.add_range(to_value=100).set_unit("mi")

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['geo']

        self.assertEqual(2, results[0]['doc_count'])

if __name__ == '__main__':
    unittest.main()
