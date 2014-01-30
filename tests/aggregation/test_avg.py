from pylastica.aggregation.avg import Avg
from pylastica.query.query import Query
from tests.base import Base

__author__ = 'Joe Linn'

import unittest
import pylastica


class AvgTest(unittest.TestCase, Base):
    def setUp(self):
        super(AvgTest, self).setUp()
        self._index = self._create_index("test_aggregation_avg")
        docs = [
            pylastica.Document("1", {"price": 5}),
            pylastica.Document("2", {"price": 8}),
            pylastica.Document("3", {"price": 1}),
            pylastica.Document("4", {"price": 3})
        ]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(AvgTest, self).tearDown()
        self._index.delete()

    def test_avg_aggregation(self):
        agg = Avg("avg")
        agg.set_field("price")

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations["avg"]
        self.assertEqual((5 + 8 + 1 + 3) / 4.0, results['value'])


if __name__ == '__main__':
    unittest.main()
