__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class MyTestCase(unittest.TestCase, Base):
    def test_to_dict(self):
        bool_filter = pylastica.filter.Bool()
        #test an empty filter
        expected = {
            'bool': {

            }
        }
        self.assertEqual(expected, bool_filter.to_dict())

        #add two filters to the 'must' clause and test
        ids_filter = pylastica.filter.Ids()
        ids_filter.set_ids('12')
        bool_filter.add_must(ids_filter)
        bool_filter.add_must(ids_filter)
        expected = {
            'bool': {
                'must': [
                    ids_filter.to_dict(),
                    ids_filter.to_dict()
                ]
            }
        }
        self.assertEqual(expected, bool_filter.to_dict())

        #add filters to the 'should' and 'must_not' clauses and test
        bool_filter.add_should(ids_filter)
        bool_filter.add_must_not(ids_filter)
        expected = {
            'bool': {
                'must': [
                    ids_filter.to_dict(),
                    ids_filter.to_dict()
                ],
                'should': [
                    ids_filter.to_dict()
                ],
                'must_not': [
                    ids_filter.to_dict()
                ]
            }
        }
        self.assertEqual(expected, bool_filter.to_dict())

    def test_filter(self):
        index = self._create_index('bool-filter-test')
        doc_type = index.get_doc_type('test')

        doc_type.add_document(pylastica.Document(1, {'name': 'Leonardo', 'species': 'turtle'}))
        doc_type.add_document(pylastica.Document(2, {'name': 'Donatello', 'species': 'turtle'}))
        doc_type.add_document(pylastica.Document(3, {'name': 'Michelangelo', 'species': 'turtle'}))
        doc_type.add_document(pylastica.Document(4, {'name': 'Raphael', 'species': 'turtle'}))
        doc_type.add_document(pylastica.Document(5, {'name': 'Splinter', 'species': 'rat'}))
        index.refresh()

        bool_filter = pylastica.filter.Bool()
        bool_filter.add_must(pylastica.filter.Term('species', 'turtle'))
        bool_filter.add_must(pylastica.filter.Term('name', 'leonardo'))

        result_set = doc_type.search(bool_filter)
        self.assertEqual(1, len(result_set))
        index.delete()

if __name__ == '__main__':
    unittest.main()
