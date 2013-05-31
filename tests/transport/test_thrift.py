__author__ = 'Joe Linn'

import unittest
import pylastica
from ..base import *


class ThriftTest(unittest.TestCase, Base):
    def setUp(self):
        self._client = pylastica.Client(self._get_hosts()[0]['host'], 9500, transport='ThriftTransport')

    def test_construct(self):
        host = self._get_hosts()[0]['host']
        port = 9500
        client = pylastica.Client(host, port, transport='Thrift')
        self.assertEqual(host, client.get_connection().host)
        self.assertEqual(port, client.get_connection().port)

    def test_search_request(self):
        index = self._client.get_index('pylastica_test1')
        index.create(options=True)
        doc_type = index.get_doc_type('user')
        doc_type.add_document(pylastica.Document(1, {'username': 'bob', 'test': ['2', '3', '5']}))
        docs = [
            pylastica.Document(2, {'username': 'bill', 'test': ['1', '3', '6']}),
            pylastica.Document(3, {'username': 'jim', 'test': ['2', '3', '7']})
        ]
        doc_type.add_documents(docs)
        index.refresh()
        result_set = doc_type.search('jim')
        self.assertEqual(1, result_set.get_total_hits())
        index.delete()

    def test_invalid_request(self):
        index = pylastica.index.Index(self._client, 'missing_index')
        self.assertRaises(pylastica.exception.ResponseException, index.get_stats)

if __name__ == '__main__':
    unittest.main()
