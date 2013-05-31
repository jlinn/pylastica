__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class IdsTest(unittest.TestCase, Base):
    def setUp(self):
        index = self._create_index('test')
        doc_type1 = index.get_doc_type('helloworld1')
        doc_type2 = index.get_doc_type('helloworld2')
        doc_type1.add_document(pylastica.Document(1, {'name': 'hello world'}))
        doc_type1.add_document(pylastica.Document(2, {'name': 'Joe Linn'}))
        doc_type1.add_document(pylastica.Document(3, {'name': 'Linn'}))
        doc_type2.add_document(pylastica.Document(4, {'name': 'hello world again'}))
        index.refresh()
        self._doc_type = doc_type1
        self._index = index

    def tearDown(self):
        self._index.delete()

    def test_set_ids_search_single(self):
        query = pylastica.query.Ids()
        query.set_ids(['1'])
        result_set = self._doc_type.search(query)
        self.assertEqual(1, len(result_set))

    def test_set_ids_search_list(self):
        query = pylastica.query.Ids()
        query.set_ids(['1', '2'])
        result_set = self._doc_type.search(query)
        self.assertEqual(2, len(result_set))

    def test_add_ids_search_single(self):
        query = pylastica.query.Ids()
        query.add_id('3')
        result_set = self._doc_type.search(query)
        self.assertEqual(1, len(result_set))

    def test_combo_ids_search_list(self):
        query = pylastica.query.Ids()
        query.set_ids(['1', '2'])
        query.add_id('3')
        result_set = self._doc_type.search(query)
        self.assertEqual(3, len(result_set))

    def test_set_type_single_search_single(self):
        query = pylastica.query.Ids('helloworld1', ['1'])
        result_set = self._doc_type.search(query)
        self.assertEqual(1, len(result_set))

    def test_set_type_singel_search_list_doc_in_other_type(self):
        query = pylastica.query.Ids('helloworld1', ['1', '4'])
        result_set = self._doc_type.search(query)
        self.assertEqual(1, len(result_set))

if __name__ == '__main__':
    unittest.main()
