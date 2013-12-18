
__author__ = 'Joe Linn'

import unittest
from pylastica.document import Document
from tests.base import Base
from pylastica.query.simplequerystring import SimpleQueryString


class MyTestCase(unittest.TestCase, Base):
    def setUp(self):
        super(MyTestCase, self).setUp()
        self._index = self._create_index("simple_query_string_test")
        docs = [
            Document(1, {'make': 'Gibson', 'model': 'Les Paul'}),
            Document(2, {'make': 'Gibson', 'model': 'SG Standard'}),
            Document(3, {'make': 'Gibson', 'model': 'SG Supreme'}),
            Document(4, {'make': 'Gibson', 'model': 'SG Faded'}),
            Document(5, {'make': 'Fender', 'model': 'Stratocaster'})
        ]
        self._index.get_doc_type("guitars").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(MyTestCase, self).tearDown()
        self._index.delete()

    def test_to_dict(self):
        string = "this is a test"
        fields = ['field1', 'field2']
        query = SimpleQueryString(string, fields)
        query.set_default_operator(SimpleQueryString.OPERATOR_OR)
        query.set_analyzer("whitespace")

        expected = {
            "simple_query_string": {
                "query": string,
                "fields": fields,
                "analyzer": "whitespace",
                "default_operator": SimpleQueryString.OPERATOR_OR
            }
        }

        self.assertEqual(expected, query.to_dict())

    def test_query(self):
        query = SimpleQueryString("gibson +sg +-faded", ["make", "model"])
        results = self._index.search(query)

        self.assertEqual(2, results.get_total_hits())

        query.set_fields(["model"])
        results = self._index.search(query)

        self.assertEqual(0, results.get_total_hits())

if __name__ == '__main__':
    unittest.main()
