__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class MatchAllTest(unittest.TestCase, Base):
    def test_to_dict(self):
        query = pylastica.query.MatchAll()
        expected = {
            'match_all': {}
        }
        self.assertEqual(expected, query.to_dict())

    def test_match_all_indices_types(self):
        #this test assumes that your ES instance has no documents
        index1 = self._create_index('test1')
        index2 = self._create_index('test2')
        client = index1.client
        search1 = pylastica.Search(client)
        result_set1 = search1.search(pylastica.query.MatchAll())
        index1.get_doc_type('test').add_document(pylastica.Document(1, {'name': 'Linn'}))
        index2.get_doc_type('test').add_document(pylastica.Document(1, {'name': 'Linn'}))
        index1.refresh()
        index2.refresh()
        search2 = pylastica.Search(client)
        result_set2 = search2.search(pylastica.query.MatchAll())
        self.assertEqual(len(result_set1) + 2, len(result_set2))
        index2.delete()
        index1.delete()


if __name__ == '__main__':
    unittest.main()
