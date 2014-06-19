__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class MoreLikeThisTest(unittest.TestCase, Base):
    def test_search(self):
        client = self._get_client()
        index = pylastica.index.Index(client, 'test')
        index.create(options=True)
        doc_type = index.get_doc_type('helloworldmlt')
        mapping = pylastica.doc_type.Mapping(doc_type, {
            'email': {'store': 'yes', 'type': 'string', 'index': 'analyzed'},
            'content': {'store': 'yes', 'type': 'string', 'index': 'analyzed'}
        })
        mapping.set_source({'enabled': False})
        doc_type.set_mapping(mapping)
        doc_type.add_document(pylastica.Document(1000, {'email': 'testemail@gmail.com', 'content': 'This is a sample post. Hello World Fuzzy Like This!'}))
        doc_type.add_document(pylastica.Document(1001, {'email': 'nospam@gmail.com', 'content': 'This is a fake nospam email address for gmail'}))
        index.refresh()

        mlt_query = pylastica.query.MoreLikeThis()
        mlt_query.set_like_text('fake gmail sample')
        mlt_query.set_fields(['email', 'content'])
        mlt_query.set_max_query_terms(1)
        mlt_query.set_min_doc_frequency(1)
        mlt_query.set_min_term_frequency(1)

        query = pylastica.query.Query(mlt_query)
        query.set_fields(['email', 'content'])
        result_set = doc_type.search(query)
        self.assertEqual(2, len(result_set))
        index.delete()


if __name__ == '__main__':
    unittest.main()
