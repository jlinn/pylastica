__author__ = 'Joe Linn'

import unittest
from tests.base import Base
import pylastica


class CommonTest(unittest.TestCase, Base):
    def test_to_dict(self):
        query = pylastica.query.Common('body', 'test query', .001)
        query.set_low_frequency_operator(pylastica.query.Common.OPERATOR_AND)

        expected = {
            'common': {
                'body': {
                    'query': 'test query',
                    'cutoff_frequency': .001,
                    'low_freq_operator': 'and'
                }
            }
        }

        self.assertEqual(expected, query.to_dict())

    def test_query(self):
        index = self._create_index('common_test')
        doc_type = index.get_doc_type('test')

        #add documents to create common terms
        doc_type.add_documents([pylastica.Document(i, {'body': 'foo bar'}) for i in xrange(5)])

        doc_type.add_document(pylastica.Document(5, {'body': 'foo baz'}))
        doc_type.add_document(pylastica.Document(6, {'body': 'foo bar baz'}))
        index.refresh()

        query = pylastica.query.Common('body', 'foo bar baz', .5)
        results = doc_type.search(query).results

        #documents containing only common words should not be returned
        self.assertEqual(2, len(results))

        #the document containing both common words should be scored lowest
        self.assertEqual(results[0].data['body'], 'foo baz')

        index.delete()


if __name__ == '__main__':
    unittest.main()
