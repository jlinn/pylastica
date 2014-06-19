__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class TermTest(unittest.TestCase, Base):
    _index = None
    """@type _index: pylastica.index.Index"""

    def setUp(self):
        super(TermTest, self).setUp()
        self._index = self._create_index("test_suggest")
        docs = [
            pylastica.Document(1, {'test': 'GitHub'}),
            pylastica.Document(2, {'test': 'Elastic'}),
            pylastica.Document(3, {'test': 'Search'}),
            pylastica.Document(4, {'test': 'Food'}),
            pylastica.Document(4, {'test': 'Flood'}),
            pylastica.Document(5, {'test': 'Folks'}),
        ]
        self._index.get_doc_type("testSuggestType").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(TermTest, self).tearDown()
        self._index.delete()

    def test_to_dict(self):
        suggest = pylastica.suggest.Suggest()
        term_suggest = pylastica.suggest.Term("suggest1", "_all")
        suggest.add_suggestion(term_suggest.set_text("Foor"))
        term_suggest2 = pylastica.suggest.Term("suggest2", "_all")
        suggest.add_suggestion(term_suggest2.set_text("Girhub"))

        expected = {
            'suggest': {
                'suggest1': {
                    'term': {
                        'field': '_all'
                    },
                    'text': 'Foor'
                },
                'suggest2': {
                    'term': {
                        'field': '_all'
                    },
                    'text': 'Girhub'
                }
            }
        }

        self.assertEqual(expected, suggest.to_dict())

    def test_suggest_results(self):
        suggest = pylastica.suggest.Suggest()
        term_suggest = pylastica.suggest.Term("suggest1", "_all")
        suggest.add_suggestion(term_suggest.set_text("Foor seach"))
        term_suggest2 = pylastica.suggest.Term("suggest2", "_all")
        suggest.add_suggestion(term_suggest2.set_text("Girhub"))

        suggests = self._index.search(suggest).suggests

        # Ensure that two suggestion results are returned for suggest1
        self.assertEqual(2, len(suggests['suggest1']))

        self.assertEqual('github', suggests['suggest2'][0]['options'][0]['text'])
        self.assertEqual('food', suggests['suggest1'][0]['options'][0]['text'])

    def test_suggest_no_results(self):
        suggest = pylastica.suggest.Suggest()
        term_suggest = pylastica.suggest.Term("suggest1", "_all")
        suggest.add_suggestion(term_suggest.set_text("Foobar").set_size(4))

        suggests = self._index.search(suggest).suggests

        # Assert that no suggestions were returned
        self.assertEqual(0, len(suggests['suggest1'][0]['options']))

if __name__ == '__main__':
    unittest.main()
