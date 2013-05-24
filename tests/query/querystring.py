__author__ = 'Joe Linn'

import unittest
import hashlib
import random
import pylastica
from ..base import *


class QueryStringTest(unittest.TestCase, Base):
    def test_search_multiple_fields(self):
        string = hashlib.md5(str(random.random())).hexdigest()
        query = pylastica.query.QueryString(string)
        expected = {'query': string}
        self.assertEqual({'query_string': expected}, query.to_dict())

        fields = [hashlib.md5(str(random.random())).hexdigest() for i in range(random.randint(0, 12) + 1)]
        query.set_fields(fields)
        expected['fields'] = fields
        self.assertEqual({'query_string': expected}, query.to_dict())

        for val in [True, False]:
            query.set_use_dis_max(val)
            expected['use_dis_max'] = val
            self.assertEqual({'query_string': expected}, query.to_dict())

    def test_search(self):
        client = self._get_client()
        index = client.get_index('test')
        index.create(options=True)
        index.settings.set_number_of_replicas(0)

        doc_type = index.get_doc_type('helloworld')
        doc_type.add_document(pylastica.Document(1, {'email': 'test@test.com', 'username': 'bobloblaw', 'test': ['2', '3', '5']}))
        index.refresh()

        query = pylastica.query.QueryString()
        query.set_query('test*')
        result_set = doc_type.search(query)
        self.assertEqual(1, len(result_set))
        index.delete()

    def test_search_fields(self):
        index = self._create_index()
        doc_type = index.get_doc_type('test')
        doc_type.add_document(pylastica.Document(1, {'title': 'hello world', 'firstname': 'Joe', 'lastname': 'Linn', 'price': '102', 'year': '2013'}))
        index.refresh()

        query = pylastica.query.QueryString()
        query.set_query('lin*').set_default_field('title')
        query.set_fields(['title', 'firstname', 'lastname', 'price', 'year'])
        result_set = doc_type.search(query)
        self.assertEqual(1, len(result_set))
        index.delete()

    def test_set_default_operator(self):
        operator = 'AND'
        query = pylastica.query.QueryString('test')
        query.set_default_operator(operator)
        self.assertEqual(query.to_dict()['query_string']['default_operator'], operator)

if __name__ == '__main__':
    unittest.main()
