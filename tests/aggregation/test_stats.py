from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.stats import Stats
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class StatsTest(unittest.TestCase, Base):
    def setUp(self):
        super(StatsTest, self).setUp()
        self._index = self._create_index("test_aggregation_stats")
        docs = [
            Document("1", {"price": 5}),
            Document("2", {"price": 8}),
            Document("3", {"price": 1}),
            Document("4", {"price": 3})
        ]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(StatsTest, self).tearDown()
        self._index.delete()

    def test_stats_aggregation(self):
        agg = Stats("stats")
        agg.set_field("price")

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['stats']

        self.assertEqual(4, results['count'])
        self.assertEqual(1, results['min'])
        self.assertEqual(8, results['max'])
        self.assertEqual((5 + 8 + 1 + 3) / 4.0, results['avg'])
        self.assertEqual((5 + 8 + 1 + 3), results['sum'])


if __name__ == '__main__':
    unittest.main()
