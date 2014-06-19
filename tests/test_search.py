from random import randint
from pylastica.query.filtered import Filtered
from pylastica.query.query import Query
from pylastica.document import Document

__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class SearchTest(unittest.TestCase, Base):
    def test_add_index(self):
        client = self._get_client()
        search = pylastica.Search(client)

        index1 = self._create_index('test1')
        index2 = self._create_index('test2')

        search.add_index(index1)
        indices = search.indices
        self.assertEqual(1, len(indices))

        search.add_index(index2)
        indices = search.indices
        self.assertEqual(2, len(indices))

        self.assertTrue(index1.name in indices)
        self.assertTrue(index2.name in indices)

        search.add_index('test3')
        indices = search.indices
        self.assertEqual(3, len(indices))
        self.assertTrue('test3' in indices)

        index1.delete()
        index2.delete()

    def test_add_indices(self):
        client = self._get_client()
        search = pylastica.Search(client)

        indices = [
            client.get_index('pylastica_test1'),
            client.get_index('pylastica_test2')
        ]

        search.add_indices(indices)
        self.assertEqual(2, len(search.indices))

    def test_search_scroll_request(self):
        client = self._get_client()
        search = pylastica.Search(client)

        index = self._create_index('test')
        doc_type = index.get_doc_type('hello')

        result = search.search(options={
            pylastica.Search.OPTION_SEARCH_TYPE: pylastica.Search.SEARCH_TYPE_SCAN,
            pylastica.Search.OPTION_SCROLL: '5m'
        })
        self.assertFalse(result.response.has_error())

        scroll_id = result.response.scroll_id
        result = search.search(options={
            pylastica.Search.OPTION_SCROLL_ID: scroll_id
        })
        self.assertFalse(result.response.has_error())
        index.delete()

    def test_scroll(self):
        search = pylastica.Search(self._get_client())

        index = self._create_index("test_scroll")
        doc_type = index.get_doc_type("test")
        doc_type.add_documents([Document(i, {"clicks": randint(0, 100)}) for i in range(0, 100)])
        index.refresh()

        search.add_index(index)
        doc_ids = set()
        for result in search.scroll("2m", options={"size": 11}):
            doc_ids.add(result.get_id())

        self.assertEqual(100, len(doc_ids))

if __name__ == '__main__':
    unittest.main()
