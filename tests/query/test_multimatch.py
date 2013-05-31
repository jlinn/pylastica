__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class MultiMatchTest(unittest.TestCase, Base):
    def test_query(self):
        client = self._get_client()
        index = pylastica.index.Index(client, 'test')
        index.create(options=True)
        doc_type = index.get_doc_type('multi_match')
        doc_type.add_document(pylastica.Document(1, {'id': 1, 'name': 'Tyler', 'last_name': 'Durden'}))
        index.refresh()

        multi_match = pylastica.query.MultiMatch()
        query = pylastica.query.Query()
        multi_match.set_query('Tyler')
        multi_match.set_fields(['name', 'last_name'])
        query.query = multi_match
        result_set = index.search(query)
        self.assertEqual(1, len(result_set))

        multi_match.set_query('Durden')
        multi_match.set_fields(['name', 'last_name'])
        query.query = multi_match
        result_set = index.search(query)
        self.assertEqual(1, len(result_set))
        index.delete()


if __name__ == '__main__':
    unittest.main()
