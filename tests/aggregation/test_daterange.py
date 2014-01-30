from pylastica.query import Query
from pylastica.aggregation.daterange import DateRange
from pylastica.doc_type import Mapping
from pylastica.document import Document
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class DateRangeTest(unittest.TestCase, Base):
    def setUp(self):
        super(DateRangeTest, self).setUp()
        self._index = self._create_index("test_aggregation_date_range")
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
        super(DateRangeTest, self).tearDown()
        self._index.delete()

    def test_date_range_aggregation(self):
        agg = DateRange("date")
        agg.set_field("created")
        agg.add_range(from_value=1390958535000).add_range(to_value=1390958535000)

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['date']

        for bucket in results:
            if 'to' in bucket:
                self.assertEqual(1, bucket['doc_count'])
            elif 'from' in bucket:
                self.assertEqual(2, bucket['doc_count'])

if __name__ == '__main__':
    unittest.main()
