from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.terms import Terms
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class TermsTest(unittest.TestCase, Base):
    def setUp(self):
        super(TermsTest, self).setUp()
        self._index = self._create_index("test_aggregation_terms")
        docs = [
            Document("1", {"price": 5, "color": "blue"}),
            Document("2", {"price": 8, "color": "blue"}),
            Document("3", {"price": 1, "color": "red"}),
            Document("4", {"price": 3, "color": "green"})
        ]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(TermsTest, self).tearDown()
        self._index.delete()

    def test_terms_aggregation(self):
        agg = Terms("terms").set_field("color")
        query = Query()
        query.add_aggregation(agg)

        results = self._index.search(query).aggregations['terms']

        self.assertEqual(2, results['buckets'][0]['doc_count'])
        self.assertEqual("blue", results['buckets'][0]['key'])


if __name__ == '__main__':
    unittest.main()
