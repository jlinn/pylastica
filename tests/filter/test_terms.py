__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class TermsTest(unittest.TestCase, Base):
    def test_lookup(self):
        index = self._create_index('test')
        doc_type1 = index.get_doc_type('band')
        doc_type2 = index.get_doc_type('members')

        doc_type1.add_document(pylastica.Document(1, {'name': 'robert'}))
        doc_type1.add_document(pylastica.Document(2, {'name': 'jimmy'}))
        doc_type1.add_document(pylastica.Document(3, {'name': 'john'}))
        doc_type1.add_document(pylastica.Document(4, {'name': 'john'}))

        doc_type2.add_document(pylastica.Document(1, {'names': ['john', 'robert']}))
        index.refresh()

        terms_filter = pylastica.filter.Terms()
        terms_filter.set_lookup('name', 'members', '1', 'names', index)
        query = pylastica.query.Query()
        query.set_filter(terms_filter)
        results = index.search(query)

        self.assertEqual(len(results.results), 3)
        index.delete()

if __name__ == '__main__':
    unittest.main()
