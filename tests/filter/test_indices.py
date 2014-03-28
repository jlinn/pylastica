from pylastica.document import Document
from pylastica.filter.boolnot import BoolNot
from pylastica.filter.indices import Indices
from pylastica.filter.term import Term
from pylastica.query.query import Query
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class IndicesTest(unittest.TestCase, Base):
    def setUp(self):
        super(IndicesTest, self).setUp()
        self._index1 = self._create_index("indices_filter_1")
        self._index2 = self._create_index("indices_filter_2")
        self._index1.add_alias("indices_filter")
        self._index2.add_alias("indices_filter")
        docs = [
            Document("1", {"color": "blue"}),
            Document("2", {"color": "green"}),
            Document("3", {"color": "blue"}),
            Document("4", {"color": "yellow"}),
        ]
        self._index1.get_doc_type("test").add_documents(docs)
        self._index2.get_doc_type("test").add_documents(docs)
        self._index1.refresh()
        self._index2.refresh()

    def tearDown(self):
        self._index1.delete()
        self._index2.delete()
        super(IndicesTest, self).tearDown()

    def test_indices_filter(self):
        indices_filter = Indices(BoolNot(Term("color", "blue")), [self._index1.name])
        indices_filter.set_no_match_filter(BoolNot(Term("color", "yellow")))
        query = Query().set_filter(indices_filter)

        # search over the alias
        index = self._get_client().get_index("indices_filter")
        results = index.search(query)

        # ensure that the proper docs have been filtered out for each index
        self.assertEqual(5, len(results))
        for result in results.results:
            data = result.data
            color = data['color']
            if result.get_index() == self._index1.name:
                self.assertNotEqual("blue", color)
            else:
                self.assertNotEqual("yellow", color)

if __name__ == '__main__':
    unittest.main()
