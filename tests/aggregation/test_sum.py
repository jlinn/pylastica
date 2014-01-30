from pylastica.query import Query
from pylastica.aggregation.sum import Sum
from tests.base import Base

__author__ = 'Joe Linn'

import unittest
import pylastica


class SumTest(unittest.TestCase, Base):
    def setUp(self):
        super(SumTest, self).setUp()
        self._index = self._create_index("test_aggregation_sum")
        docs = [
            pylastica.Document("1", {"price": 5}),
            pylastica.Document("2", {"price": 8}),
            pylastica.Document("3", {"price": 1}),
            pylastica.Document("4", {"price": 3})
        ]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(SumTest, self).tearDown()
        self._index.delete()

    def test_sum_aggregation(self):
        agg = Sum("sum")
        agg.set_field("price")

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations["sum"]
        self.assertEqual(5 + 8 + 1 + 3, results['value'])


if __name__ == '__main__':
    unittest.main()
