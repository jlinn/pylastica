from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.valuecount import ValueCount
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class ValueCountTest(unittest.TestCase, Base):
    def setUp(self):
        super(ValueCountTest, self).setUp()
        self._index = self._create_index("test_aggregation_value_count")
        docs = [
            Document("1", {"price": 5}),
            Document("2", {"price": 8}),
            Document("3", {"price": 1}),
            Document("4", {"price": 3}),
            Document("5", {"price": 3})
        ]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(ValueCountTest, self).tearDown()
        self._index.delete()

    def test_value_count_aggregation(self):
        agg = ValueCount("count", "price")

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['count']

        self.assertEqual(5, results['value'])

if __name__ == '__main__':
    unittest.main()
