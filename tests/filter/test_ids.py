__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class IdsTest(unittest.TestCase, Base):
    def setUp(self):
        index = self._create_index('test')
        doc_type1 = index.get_doc_type('helloworld1')
        doc_type2 = index.get_doc_type('helloworld2')

        doc_type1.add_documents([pylastica.Document(i, {'name': 'Linn'}) for i in range(100)])
        doc_type2.add_documents([pylastica.Document(i, {'name': 'Linn'}) for i in range(100)])

        doc_type2.add_document(pylastica.Document(101, {'name': 'Linn'}))
        index.optimize()
        index.refresh()
        self._doc_type = doc_type1
        self._index = index

    def tearDown(self):
        self._index.delete()

    def test_set_ids_search_single(self):
        ids_filter = pylastica.filter.Ids().set_ids('1')
        query = pylastica.query.Query.create(ids_filter)
        self.assertEqual(1, len(self._doc_type.search(query)))

    def test_set_ids_search_multiple(self):
        ids_filter = pylastica.filter.Ids()
        ids_filter.set_ids(['1', '7', '13'])
        query = pylastica.query.Query.create(ids_filter)
        self.assertEqual(3, len(self._doc_type.search(query)))

    def test_combo_ids_search(self):
        ids_filter = pylastica.filter.Ids()
        ids_filter.set_ids(['1', '7', '13'])
        ids_filter.add_id('39')
        query = pylastica.query.Query.create(ids_filter)
        self.assertEqual(4, len(self._doc_type.search(query)))

    def test_set_type_list_search_single(self):
        ids_filter = pylastica.filter.Ids()
        ids_filter.set_ids('4')
        ids_filter.set_doc_type(['helloworld1', 'helloworld2'])
        query = pylastica.query.Query.create(ids_filter)
        self.assertEqual(2, len(self._index.search(query)))

if __name__ == '__main__':
    unittest.main()
