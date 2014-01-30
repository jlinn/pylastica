from pylastica.query import Query
from pylastica import Document
from pylastica.aggregation.datehistogram import DateHistogram
from pylastica.doc_type import Mapping
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class DateHistogramTest(unittest.TestCase, Base):
    def setUp(self):
        super(DateHistogramTest, self).setUp()
        self._index = self._create_index("test_aggregation_date_histogram")
        mapping = Mapping()
        mapping.set_properties({
            "created": {"type": "date"}
        })
        doc_type = self._index.get_doc_type("test")
        doc_type.mapping = mapping
        docs = [
            Document("1", {"created": 1390962135000}),
            Document("2", {"created": 1390965735000}),
            Document("3", {"created": 1390954935000})
        ]
        doc_type.add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(DateHistogramTest, self).tearDown()
        self._index.delete()

    def test_date_histogram_aggregation(self):
        agg = DateHistogram("hist", "created", "1h")

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['hist']

        self.assertEqual(3, len(results))


if __name__ == '__main__':
    unittest.main()
