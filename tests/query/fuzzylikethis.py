__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class FuzzyLikeThisTest(unittest.TestCase, Base):
    def test_search(self):
        index = self._create_index()
        doc_type = index.get_doc_type('helloworldfuzzy')
        mapping = pylastica.doc_type.Mapping(doc_type, {
            'email': {'store': 'yes', 'type': 'string', 'index': 'analyzed'},
            'content': {'store': 'yes', 'type': 'string', 'index': 'analyzed'}
        })
        mapping.set_source({'enabled': False})
        doc_type.mapping = mapping
        doc_type.add_document(pylastica.Document(1000, {'email': 'test@gmail.com', 'content': 'This is a sample post. Hello World Fuzzy Like This!'}))
        index.refresh()

        flt_query = pylastica.query.FuzzyLikeThis().set_like_text('sample gmail')
        flt_query.set_fields(['email', 'content'])
        flt_query.set_min_similarity(.3)
        flt_query.set_max_query_terms(3)
        result_set = doc_type.search(flt_query)
        self.assertEqual(1, len(result_set))
        index.delete()


if __name__ == '__main__':
    unittest.main()
