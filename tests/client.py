__author__ = 'Joe Linn'

import unittest
import pylastica

class TestClient(unittest.TestCase):
    def test_connections(self):
        client = self._get_client()
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
            self.assertEqual(result.get_data()['username'], 'joe')
        index.delete()

    def test_two_servers_one_client(self):
        client = pylastica.Client(connections=[
            {'host': 'es1.vr', 'port': 9200},
            {'host': 'es2.vr', 'port': 9200}
        ])
        index = client.get_index('pylastica_test1')
        index.create(options=True)
        doc_type = index.get_doc_type('user')

        #add a document to the index
        doc_1 = pylastica.Document(1, {
            'username': 'joe',
            'test':['1', '3', '5']
        })
        doc_type.add_document(doc_1)

        #add multiple documents using the _bulk protocol
        docs = [
            pylastica.Document(2, {'username': 'bob', 'test': ['2', '4', '6']}),
            pylastica.Document(3, {'username': 'foo', 'test': ['3', '5', '7']})
        ]
        doc_type.add_documents(docs)
        index.refresh()
        result_set = doc_type.search('bob')
        for result in result_set:
            self.assertEqual(result.get_data()['username'], 'bob')
        index.delete()

    def test_bulk(self):
        client = self._get_client()
        params = [
            {'index': {'_index': 'test', '_type': 'user', '_id': '1'}},
            {'user': {'name': 'joe'}},
            {'index': {'_index': 'test', '_type': 'user', '_id': '2'}},
            {'user': {'name': 'bob'}}
        ]
        client.bulk(params)
        index = client.get_index('test')
        result_set = index.search('joe')
        for result in result_set:
            self.assertEqual(result.get_data()['user']['name'], 'joe')
        index.delete()

    def test_optimize_all(self):
        client = self._get_client()
        response = client.optimize_all()
        self.assertFalse(response.has_error())

    def test_add_documents_empty(self):
        client = self._get_client()
        self.assertRaises(AssertionError, client.add_documents, [])

    def test_delete_ids_index_string_type_string(self):
        data = {'username': 'joe'}
        user_search = 'username:joe'
        index = self._create_index()
        doc_type = index.get_doc_type('user')

        #add a document to the index
        doc = pylastica.document.Document(data=data)
        result = doc_type.add_document(doc)
        index.refresh()

        result_data = result.get_data()
        ids = [result_data['_id']]

        #ensure that the document is in the index
        result_set = doc_type.search(user_search)
        total_hits = result_set.get_total_hits()
        self.assertEqual(1, total_hits)

        #verify that the variables we are going to send to delete_ids are the type for which we're testing
        index_string = index.name
        doc_type_string = doc_type.name
        self.assertIsInstance(index_string, str)
        self.assertIsInstance(doc_type_string, str)

        response = index.client.delete_ids(ids, index, doc_type)
        index.refresh()
        #verify that the document has been deleted
        result_set = doc_type.search(user_search)
        self.assertEqual(0, result_set.get_total_hits())
        index.delete()

    def test_delete_ids_index_string_type_object(self):
        data = {'username': 'joe'}
        user_search = 'username:joe'
        index = self._create_index()
        doc_type = index.get_doc_type('user')
        doc = pylastica.Document(data=data)
        result = doc_type.add_document(doc)
        index.refresh()
        result_data = result.get_data()
        ids = [result_data['_id']]

        #ensure that the document is in the index
        result_set = doc_type.search(user_search)
        self.assertEqual(1, result_set.get_total_hits())

        index_string = index.name
        self.assertIsInstance(index_string, str)
        self.assertIsInstance(doc_type, pylastica.doc_type.DocType)

        #delete the document using the index string and doc_type object
        response = index.client.delete_ids(ids, index, doc_type)
        index.refresh()

        result_set = doc_type.search(user_search)
        self.assertEqual(0, result_set.get_total_hits())

    def test_one_invalid_connection(self):
        client = self._get_client()
        connection_1 = pylastica.Connection({'host': 'es1.vr', 'timeout': 2})
        connection_2 = pylastica.Connection({'host': 'es10.vr', 'timeout': 2})

        client.connections = [connection_2, connection_1]
        client.request('_status', pylastica.Request.GET)
        connections = client.connections
        self.assertEqual(2, len(connections))
        self.assertTrue(not connections[0].is_enabled() or not connections[1].is_enabled())

    def test_two_invalid_connections(self):
        client = self._get_client()
        connection_1 = pylastica.Connection({'host': 'foo.vr', 'timeout': 2})
        connection_2 = pylastica.Connection({'host': 'bar.vr', 'timeout': 2})
        client.connections = [connection_1, connection_2]
        self.assertRaises(pylastica.exception.ClientException, client.request, '_status', pylastica.Request.GET)
        connections = client.connections
        self.assertEqual(2, len(connections))
        self.assertTrue(not connections[0].enabled and not connections[1].enabled)

    def test_callback(self):
        def callback(connection, exception):
            self.assertIsInstance(connection, pylastica.Connection)
            self.assertIsInstance(exception, pylastica.exception.ConnectionException)
            self.assertFalse(connection.enabled)
            callback.count += 1

        callback.count = 0
        client = pylastica.Client('es1.vr', callback=callback)
        connection_1 = pylastica.Connection({'host': 'foo.vr', 'timeout': 2})
        connection_2 = pylastica.Connection({'host': 'bar.vr', 'timeout': 2})
        client.connections = [connection_1, connection_2]
        self.assertEqual(0, callback.count)
        self.assertRaises(pylastica.exception.ClientException, client.request, '_status', pylastica.Request.GET)
        self.assertEqual(2, callback.count)

    def test_update_document_by_document(self):
        index = self._create_index()
        doc_type = index.get_doc_type('test')
        client = index.client
        new_document = pylastica.Document(1, {'field1': 'value1', 'field2': 'value2'})
        doc_type.add_document(new_document)
        update_document = pylastica.Document(1, {'field2': 'value2changed', 'field3': 'value3added'})
        client.update_document(1, update_document, index.name, doc_type.name)
        document = doc_type.get_document(1)

        self.assertIsInstance(document, pylastica.Document)
        data = document.data
        self.assertTrue('field1' in data)
        self.assertEqual('value1', data['field1'])
        self.assertTrue('field2' in data)
        self.assertEqual('value2changed', data['field2'])
        self.assertTrue('field3' in data)
        self.assertEqual('value3added', data['field3'])
        index.delete()

    def test_update_document_by_document_with_script(self):
        index = self._create_index()
        doc_type = index.get_doc_type('test')
        client = index.client
        new_document = pylastica.Document(1, {'field1': 'value1', 'field2': 10, 'field3': 'should be removed', 'field4': 'value4'})
        script = pylastica.Script('ctx._source.field2 += count; ctx._source.remove("field3"); ctx._source.field4 = "changed";')
        script.set_param('count', 5)
        new_document.script = script
        #should use document, not script, because document does not exist
        client.update_document(1, new_document, index.name, doc_type.name, {'fields': '_source'})
        document = doc_type.get_document(1)

        self.assertIsInstance(document, pylastica.Document)
        data = document.data
        self.assertTrue('field1' in data)
        self.assertEqual('value1', data['field1'])
        self.assertTrue('field2' in data)
        self.assertEqual(10, data['field2'])
        self.assertTrue('field4' in data)
        self.assertEqual('value4', data['field4'])
        self.assertTrue('field3' in data)

        #should use script this time, because the document exists
        client.update_document(1, new_document, index.name, doc_type.name, {'fields': '_source'})
        document = doc_type.get_document(1)
        self.assertIsInstance(document, pylastica.Document)
        data = document.data
        self.assertTrue('field1' in data)
        self.assertEqual('value1', data['field1'])
        self.assertTrue('field2' in data)
        self.assertEqual(15, data['field2'])
        self.assertTrue('field4' in data)
        self.assertEquals('changed', data['field4'])
        self.assertFalse('field3' in data)
        index.delete()

    def test_update_document_by_raw_data(self):
        index = self._create_index()
        doc_type = index.get_doc_type('test')
        client = index.client
        new_document = pylastica.Document(1, {'field1': 'value1'})
        doc_type.add_document(new_document)

        raw_data = {
            'doc':{
                'field2': 'value2'
            }
        }
        response = client.update_document(1, raw_data, index.name, doc_type.name, {'retry_on_conflict': 1})
        self.assertTrue(response.is_ok())

        document = doc_type.get_document(1)
        self.assertIsInstance(document, pylastica.Document)
        data = document.data
        self.assertTrue('field1' in data)
        self.assertEqual('value1', data['field1'])
        self.assertTrue('field2' in data)
        self.assertEqual('value2', data['field2'])
        index.delete()

    def test_add_document_without_ids(self):
        docs = [pylastica.Document(data={'post': i}) for i in range(10)]
        for doc in docs:
            self.assertFalse(doc.has_id())
        index = self._create_index()
        client = index.client
        client.set_config_value('document', {'autoPopulate': True})
        doc_type = index.get_doc_type('pos')
        doc_type.add_documents(docs)
        for doc in docs:
            self.assertTrue(doc.has_id())
            self.assertTrue(doc.has_version())
            self.assertEqual(1, doc.version)
        index.delete()

    def _get_client(self):
        return pylastica.Client('es1.vr')

    def _create_index(self, name='test'):
        """
        Create a test index
        @param name: name of the index
        @type name: str
        @return:
        @rtype: pylastica.index.Index
        """
        client = self._get_client()
        index = client.get_index("pylastica_%s" % name)
        index.create({'index': {'number_of_shards': 1, 'number_of_replicas': 0}}, True)
        return index

if __name__ == '__main__':
    unittest.main()
