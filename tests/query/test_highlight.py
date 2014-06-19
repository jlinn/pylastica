__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class HighlightTest(unittest.TestCase, Base):
    def test_highlight_search(self):
        index = self._create_index()
        doc_type = index.get_doc_type('helloworld')
        phrase = 'My name is Joe'
        doc_type.add_document(pylastica.Document(1, {'id': 1, 'phrase': phrase, 'username': 'bobloblaw', 'test': ['2', '3', '5']}))
        doc_type.add_document(pylastica.Document(2, {'id': 2, 'phrase': phrase, 'username': 'peter', 'test': ['2', '3', '5']}))
        index.refresh()

        query_string = pylastica.query.QueryString('jo*')
        query = pylastica.query.Query(query_string)
        query.set_highlight({
            'pre_tags': ['<em class="highlight">'],
            'post_tags': ['</em>'],
            'fields': {
                'phrase': {
                    'fragment_size': 200,
                    'number_of_fragments': 1
                }
            }
        })
        result_set = doc_type.search(query)
        for result in result_set:
            highlight = result.get_highlights()
            self.assertEqual({'phrase': ['My name is <em class="highlight">Joe</em>']}, highlight)
        self.assertEqual(2, len(result_set))
        index.delete()


if __name__ == '__main__':
    unittest.main()
