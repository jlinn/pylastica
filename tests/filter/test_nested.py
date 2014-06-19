__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class MyTestCase(unittest.TestCase, Base):
    def setUp(self):
        index = self._create_index('pylastica_test_filter_nested')
        doc_type = index.get_doc_type('user')
        mapping = pylastica.doc_type.Mapping()
        mapping.set_properties({
            'firstname': {'type': 'string', 'store': 'yes'},
            'lastname': {'type': 'string'},
            'hobbies': {
                'type': 'nested',
                'include_in_parent': True,
                'properties': {
                    'hobby': {'type': 'string'}
                }
            }
        })
        doc_type.mapping = mapping
        doc_type.add_documents([
            pylastica.Document(1, {
                'firstname': 'Andrew',
                'lastname': 'Wiggin',
                'hobbies': [
                    {'hobby': 'games'}
                ]
            }),
            pylastica.Document(2, {
                'firstname': 'Bonzo',
                'lastname': 'Madrid',
                'hobbies': [
                    {'hobby': 'games'},
                    {'hobby': 'bullying'}
                ]
            })
        ])
        index.refresh()
        self._index = index
        self._doc_type = doc_type

    def tearDown(self):
        self._index.delete()

    def test_nested(self):
        f = pylastica.filter.Nested()
        self.assertEqual({'nested': {}}, f.to_dict())
        q = pylastica.query.Terms()
        q.set_terms('hobby', ['bullying'])
        f.set_path('hobbies')
        f.set_query(q)

        result = self._doc_type.search(f)
        self.assertEqual(1, result.get_total_hits())

        f = pylastica.filter.Nested()
        q = pylastica.query.Terms()
        q.set_terms('hobby', ['games'])
        f.set_path('hobbies')
        f.set_query(q)

        result = self._doc_type.search(f)
        self.assertEqual(2, result.get_total_hits())

if __name__ == '__main__':
    unittest.main()
