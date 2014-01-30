from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.avg import Avg
from pylastica.aggregation.filter import Filter
from pylastica.filter.range import Range
from pylastica.filter.term import Term
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class FilterTest(unittest.TestCase, Base):
    def setUp(self):
        super(FilterTest, self).setUp()
        self._index = self._create_index("test_aggregation_filter")
        docs = [
            Document("1", {"price": 5, "color": "blue"}),
            Document("2", {"price": 8, "color": "blue"}),
            Document("3", {"price": 1, "color": "red"}),
            Document("4", {"price": 3, "color": "green"})
        ]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(FilterTest, self).tearDown()
        self._index.delete()

    def test_to_dict(self):
        expected = {
            "filter": {"range": {"stock": {"gt": 0}}},
            "aggs": {
                "avg_price": {"avg": {"field": "price"}}
            }
        }

        agg = Filter("in_stock_products").set_filter(Range("stock", {"gt": 0}))
        agg.add_aggregation(Avg("avg_price").set_field("price"))

        self.assertEqual(expected, agg.to_dict())

    def test_filter_aggregation(self):
        agg = Filter("filter").set_filter(Term("color", "blue")).add_aggregation(Avg("price").set_field("price"))

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['filter']['price']['value']

        self.assertEqual((5 + 8) / 2.0, results)


if __name__ == '__main__':
    unittest.main()
