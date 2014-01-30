from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.missing import Missing
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class MissingTest(unittest.TestCase, Base):
    def setUp(self):
        super(MissingTest, self).setUp()
        self._index = self._create_index("test_aggregation_missing")
        docs = [
            Document("1", {"price": 5, "color": "blue"}),
            Document("2", {"price": 8, "color": "blue"}),
            Document("3", {"price": 1}),
            Document("4", {"price": 3, "color": "green"})
        ]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(MissingTest, self).tearDown()
        self._index.delete()

    def test_missing_aggregation(self):
        agg = Missing("missing").set_field("color")

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['missing']

        self.assertEqual(1, results['doc_count'])


if __name__ == '__main__':
    unittest.main()
