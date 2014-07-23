from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.terms import Terms
from pylastica.aggregation.tophits import TopHits
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class TopHitsTest(unittest.TestCase, Base):
    def setUp(self):
        super(TopHitsTest, self).setUp()
        self._index = self._create_index("test_aggregation_top_hits")
        docs = [Document(i, {"price": 5}) for i in range(0, 5)]
        docs += [Document(i, {"price": 4}) for i in range(5, 8)]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        self._index.delete()
        super(TopHitsTest, self).tearDown()

    def test_top_hits_aggregation(self):
        agg = Terms("terms").set_field("price")
        agg.add_aggregation(TopHits("hits").set_size(5))
        query = Query()
        query.add_aggregation(agg)

        results = self._index.search(query).aggregations['terms']["buckets"]

        self.assertEqual(2, len(results))
        self.assertEqual(5, len(results[0]["hits"]["hits"]["hits"]))
        for hit in results[0]['hits']['hits']['hits']:
            self.assertEqual(5, hit["_source"]["price"])

if __name__ == '__main__':
    unittest.main()
