from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.range import Range
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class RangeTest(unittest.TestCase, Base):
    def setUp(self):
        super(RangeTest, self).setUp()
        self._index = self._create_index("test_aggregation_range")
        docs = [
            Document("1", {"price": 5, "color": "blue"}),
            Document("2", {"price": 8, "color": "blue"}),
            Document("3", {"price": 1, "color": "red"}),
            Document("4", {"price": 3, "color": "green"}),
            Document("5", {"price": 1.5, "color": "green"}),
            Document("6", {"price": 2, "color": "green"})
        ]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(RangeTest, self).tearDown()
        self._index.delete()

    def test_range_aggregation(self):
        agg = Range("range")
        agg.set_field("price")
        agg.add_range(from_value=1.5, to_value=5)

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['range']['buckets']
        self.assertEqual(2, results[0]['doc_count'])

if __name__ == '__main__':
    unittest.main()
