from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.geohashgrid import Geohashgrid
from pylastica.doc_type import Mapping
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class GeohashgridTest(unittest.TestCase, Base):
    def setUp(self):
        super(GeohashgridTest, self).setUp()
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
        super(GeohashgridTest, self).tearDown()
        self._index.delete()

    def test_geohashgrid_aggregation(self):
        agg = Geohashgrid("hash", "location")
        agg.set_precision(3)

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['hash']

        self.assertEqual(2, results['buckets'][0]['doc_count'])
        self.assertEqual(1, results['buckets'][1]['doc_count'])


if __name__ == '__main__':
    unittest.main()
