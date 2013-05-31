__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class BoolAndTest(unittest.TestCase, Base):
    def test_to_dict(self):
        and_filter = pylastica.filter.BoolAnd()
        self.assertEqual({'and': {'filters': []}}, and_filter.to_dict())
        ids_filter = pylastica.filter.Ids()
        ids_filter.set_ids('12')
        and_filter.add_filter(ids_filter)
        and_filter.add_filter(ids_filter)
        expected_dict = {
            'and': {
                'filters': [
                    ids_filter.to_dict(),
                    ids_filter.to_dict()
                ]
            }
        }
        self.assertEqual(expected_dict, and_filter.to_dict())

    def test_set_cache(self):
        #create an index
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        doc_type = index.get_doc_type('test')
        #add some docs
        doc = pylastica.Document(1, {'name': 'hello world'})
        doc_type.add_document(doc)
        doc = pylastica.Document(2, {'name': 'Joe Linn'})
        doc_type.add_document(doc)
        doc_type.add_document(pylastica.Document(3, {'name': 'Linn'}))
        index.refresh()
        #create a filter
        and_filter = pylastica.filter.BoolAnd()
        ids_filter1 = pylastica.filter.Ids()
        ids_filter1.set_ids('1')
        and_filter.add_filter(ids_filter1)
        and_filter.add_filter(pylastica.filter.Ids(ids='1'))
        and_filter.set_cached()
        #run a test query
        result_set = doc_type.search(and_filter)
        self.assertEqual(1, len(result_set))
        index.delete()

if __name__ == '__main__':
    unittest.main()
