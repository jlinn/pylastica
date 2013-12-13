__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import Base


class PhraseTest(unittest.TestCase, Base):
    def setUp(self):
        super(PhraseTest, self).setUp()
        self._index = self._create_index("test_suggest_phrase")
        docs = [
            pylastica.Document(1, {'text': 'Github is pretty cool'}),
            pylastica.Document(2, {'text': 'Elasticsearch is bonsai cool'}),
            pylastica.Document(3, {'text': 'This is a test phrase'}),
            pylastica.Document(4, {'text': 'Another phrase for testing'}),
            pylastica.Document(5, {'text': 'Some more words here'})
        ]
        self._index.get_doc_type("testSuggestType").add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(PhraseTest, self).tearDown()
        self._index.delete()

    def test_to_dict(self):
        suggest = pylastica.suggest.Suggest()
        phrase_suggest = pylastica.suggest.Phrase('suggest1', 'text')
        phrase_suggest.set_text('elasticsearch is bansai coor')
        phrase_suggest.set_analyzer('simple')
        suggest.add_suggestion(phrase_suggest)
        suggest.set_global_text('global')

        expected = {
            'suggest': {
                'text': 'global',
                'suggest1': {
                    'text': 'elasticsearch is bansai coor',
                    'phrase': {
                        'field': 'text',
                        'analyzer': 'simple'
                    }
                }
            }
        }

        self.assertEqual(expected, suggest.to_dict())

    def test_phrase_suggest(self):
        suggest = pylastica.suggest.Suggest()
        phrase_suggest = pylastica.suggest.Phrase('suggest1', 'text')
        phrase_suggest.set_text('elasticsearch is bansai coor')
        phrase_suggest.set_analyzer('simple')
        phrase_suggest.set_highlight("<suggest>", "</suggest>")
        phrase_suggest.set_stupid_backoff_smoothing()
        phrase_suggest.add_candidate_generator(pylastica.suggest.candidategenerator.DirectGenerator('text'))
        suggest.add_suggestion(phrase_suggest)

        suggests = self._index.search(suggest).suggests

        self.assertEqual(3, len(suggests['suggest1'][0]['options']))

        self.assertEqual("elasticsearch is <suggest>bonsai cool</suggest>", suggests['suggest1'][0]['options'][0]['highlighted'])
        self.assertEqual("elasticsearch is bonsai cool", suggests['suggest1'][0]['options'][0]['text'])


if __name__ == '__main__':
    unittest.main()
