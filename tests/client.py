__author__ = 'Joe Linn'

import unittest
import pylastica

class TestClient(unittest.TestCase):
    def test_connections(self):
        client = pylastica.Client('es1.vr')
        index = client.get_index('pylastica_test1')
        index.create(options=True)
        doc_type = index.get_doc_type('user')
        doc_1 = pylastica.Document(1, {
            'username': 'joe',
            'test':['1', '3', '5']
        })
        doc_type.add_document(doc_1)
        docs = []
        docs.append(pylastica.document.Document(2, {'username': 'bob', 'test': ['2', '4', '6']}))
        docs.append(pylastica.document.Document(3, {'username': 'foo', 'test': ['3', '5', '7']}))
        doc_type.add_documents(docs)

        index.refresh()
        result_set = doc_type.search('joe')
        for result in result_set:
            print result.get_data()

if __name__ == '__main__':
    unittest.main()
