from pylastica.query import Query
from pylastica.aggregation.min import Min
from pylastica.aggregation.nested import Nested
from pylastica.doc_type.mapping import Mapping
from pylastica.document import Document
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class NestedTest(unittest.TestCase, Base):
    def setUp(self):
        super(NestedTest, self).setUp()
        self._index = self._create_index("test_aggregation_nested")
        mapping = Mapping()
        mapping.set_properties({
            "resellers": {
                "type": "nested",
                "properties": {
                    "name": {"type": "string"},
                    "price": {"type": "double"}
                }
            }
        })
        doc_type = self._index.get_doc_type("test")
        doc_type.mapping = mapping
        docs = [
            Document(1, {
                "resellers": {
                    "name": "spacely sprockets",
                    "price": 5.55
                }
            }),
            Document(2, {
                "resellers": {
                    "name": "cogswell cogs",
                    "price": 4.98
                }
            })
        ]
        doc_type.add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(NestedTest, self).tearDown()
        self._index.delete()

    def test_nested_aggregation(self):
        agg = Nested("resellers", "resellers")
        agg.add_aggregation(Min("min_price").set_field("price"))

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['resellers']

        self.assertEqual(4.98, results['min_price']['value'])

if __name__ == '__main__':
    unittest.main()
