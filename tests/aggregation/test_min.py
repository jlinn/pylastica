from pylastica.aggregation.min import Min
from pylastica.document import Document
from pylastica.query.query import Query
from pylastica.script import Script
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class MinTest(unittest.TestCase, Base):
    def setUp(self):
        super(MinTest, self).setUp()
        self._index = self._create_index("test_aggregation_min")
        docs = [
            Document("1", {"price": 5}),
            Document("2", {"price": 8}),
            Document("3", {"price": 1}),
            Document("4", {"price": 3})
        ]
        self._index.get_doc_type("test").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(MinTest, self).tearDown()
        self._index.delete()

    def test_to_dict(self):
        expected = {
            "min": {
                "field": "price",
                "script": "_value * conversion_rate",
                "params": {
                    "conversion_rate": 1.2
                }
            }
        }
        agg = Min("min_price_in_euros")
        agg.set_field("price")
        agg.set_script(Script("_value * conversion_rate", {"conversion_rate": 1.2}))
        self.assertEqual(expected, agg.to_dict())

    def test_min_aggregation(self):
        agg = Min("min_price")
        agg.set_field("price")

        query = Query()
        query.add_aggregation(agg)
        results = self._index.get_doc_type("test").search(query).aggregations["min_price"]
        self.assertAlmostEqual(1, results["value"])

        # test using a script
        agg.set_script(Script("_value * conversion_rate", {"conversion_rate": 1.2}))
        query = Query()
        query.add_aggregation(agg)
        results = self._index.get_doc_type("test").search(query).aggregations["min_price"]
        self.assertEqual(1.2, results["value"])

if __name__ == '__main__':
    unittest.main()
