__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class MyTestCase(unittest.TestCase, Base):
    def setUp(self):
        self._index = self._create_index('test_functionscore')
        self._doc_type = self._index.get_doc_type('test')
        self._doc_type.mapping = {
            'name': {'type': 'string', 'index': 'not_analyzed'},
            'location': {'type': 'geo_point'},
            'price': {'type': 'float'}
        }
        self._doc_type.add_document(pylastica.Document(1, {
            'name': "Mr. Frostie's",
            'location': {'lat': 32.799605, 'lon': -117.243027},
            'price': 4.5
        }))
        self._doc_type.add_document(pylastica.Document(2, {
            'name': "Miller's Field",
            'location': {'lat': 32.795964, 'lon': -117.255028},
            'price': 9.5
        }))
        self._doc_type.add_document(pylastica.Document(3, {
            'name': "Ciro's",
            'location': {'lat': 32.797026, 'lon': -117.252107},
            'price': 9.0
        }))
        self._doc_type.add_document(pylastica.Document(4, {
            'name': "Kafe Yen",
            'location': {'lat': 32.796940, 'lon': -117.256027},
            'price': 9.5
        }))
        self._doc_type.add_document(pylastica.Document(5, {
            'name': "Kato Sushi",
            'location': {'lat': 32.797460, 'lon': -117.252024},
            'price': 15
        }))
        self._doc_type.add_document(pylastica.Document(6, {
            'name': "George's At the Cove",
            'location': {'lat': 32.849437, 'lon': -117.271732},
            'price': 25
        }))
        self._index.refresh()

        self._location_origin = "32.804654, -117.242594"
        self._price_origin = 0

    def tearDown(self):
        self._index.delete()

    def test_to_dict(self):
        query = pylastica.query.FunctionScore()
        query.set_query(pylastica.query.MatchAll())
        query.add_decay_function(pylastica.query.FunctionScore.DECAY_GAUSS, 'location', self._location_origin, "2mi")
        query.add_decay_function(pylastica.query.FunctionScore.DECAY_GAUSS, 'price', self._price_origin, 9.25)
        expected = {
            'function_score': {
                'query': {
                    'match_all': {}
                },
                'functions': [
                    {
                        'gauss': {
                            'location': {
                                'origin': '32.804654, -117.242594',
                                'scale': '2mi'
                            }
                        }
                    },
                    {
                        'gauss': {
                            'price': {
                                'origin': self._price_origin,
                                'scale': 9.25
                            }
                        }
                    }
                ]
            }
        }
        self.assertEqual(query.to_dict(), expected)

    def test_gauss(self):
        query = pylastica.query.FunctionScore()
        query.add_decay_function(pylastica.query.FunctionScore.DECAY_GAUSS, 'location', self._location_origin, "4mi")
        query.add_decay_function(pylastica.query.FunctionScore.DECAY_GAUSS, 'price', self._price_origin, 10)
        response = self._doc_type.search(query)
        results = response.results

        #the document with teh closest location and lowest price should be scored highest
        self.assertEqual(results[-1].data['name'], "George's At the Cove")
        self.assertEqual(results[0].data['name'], "Mr. Frostie's")

if __name__ == '__main__':
    unittest.main()
