from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.histogram import Histogram
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class HistogramTest(unittest.TestCase, Base):
    def setUp(self):
        super(HistogramTest, self).setUp()
        self._index = self._create_index("test_aggregation_histogram")
        docs = [
            Document("1", {"price": 5, "color": "blue"}),
            Document("2", {"price": 8, "color": "blue"}),
            Document("3", {"price": 1, "color": "red"}),
            Document("4", {"price": 30, "color": "green"}),
            Document("5", {"price": 40, "color": "red"}),
            Document("6", {"price": 35, "color": "green"}),
            Document("7", {"price": 42, "color": "red"}),
            Document("8", {"price": 41, "color": "blue"})
        ]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(HistogramTest, self).tearDown()
        self._index.delete()

    def test_histogram_aggregation(self):
        agg = Histogram("hist", "price", 10)
        agg.set_minimum_document_count(0)   # should return empty buckets

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['hist']

        self.assertEqual(5, len(results))
        self.assertEqual(30, results[3]['key'])
        self.assertEqual(2, results[3]['doc_count'])

if __name__ == '__main__':
    unittest.main()
