__author__ = 'Joe Linn'

import unittest
import pylastica
from .base import Base


class BulkTest(unittest.TestCase, Base):
    def test_create_abstract_document_with_invalid_data(self):
        bad_document = object()
        # wrong class type
        self.assertRaises(TypeError, pylastica.bulk.abstractdocument.AbstractDocument.create, bad_document)

        # attempt to create a Document with a Script
        script = pylastica.Script('')
        self.assertRaises(TypeError, pylastica.bulk.abstractdocument.AbstractDocument.create, script, pylastica.bulk.abstractdocument.AbstractDocument.OP_TYPE_CREATE)

    def test_send(self):
        index = self._create_index()
        doc_type = index.get_doc_type('bulk_test')
        doc_type2 = index.get_doc_type('bulk_test2')
        client = index.client

        doc1 = doc_type.create_document(1, {'name': 'John'})
        doc2 = pylastica.Document(2, {'name': 'Paul'})
        doc3 = doc_type.create_document(3, {'name': 'George'})
        doc4 = doc_type.create_document(data={'name': 'Ringo'})
        doc1.percolate = '*'
        doc3.op_type = pylastica.Document.OP_TYPE_CREATE
        documents = [doc1, doc2, doc3, doc4]

        bulk = pylastica.bulk.Bulk(client)
        bulk.doc_type = doc_type2
        bulk.add_documents(documents)
        actions = bulk.actions

        self.assertIsInstance(actions[0], pylastica.bulk.action.IndexDocument)
        self.assertEqual('index', actions[0].op_type)
        self.assertEqual(doc1, actions[0].document)
        self.assertIsInstance(actions[1], pylastica.bulk.action.IndexDocument)
        self.assertEqual('index', actions[1].op_type)
        self.assertEqual(doc2, actions[1].document)
        self.assertIsInstance(actions[2], pylastica.bulk.action.IndexDocument)
        self.assertEqual('create', actions[2].op_type)
        self.assertEqual(doc3, actions[2].document)
        self.assertIsInstance(actions[3], pylastica.bulk.action.IndexDocument)
        self.assertEqual('index', actions[3].op_type)
        self.assertEqual(doc4, actions[3].document)

        data = bulk.to_list()
        expected = [
            {'index': {'_index': 'pylastica_test', '_type': 'bulk_test', '_id': '1', '_percolate': '*'}},
            {'name': 'John'},
            {'index': {'_id': '2', '_index': None, '_type': None}},
            {'name': 'Paul'},
            {'create': {'_index': 'pylastica_test', '_type': 'bulk_test', '_id': '3'}},
            {'name': 'George'},
            {'index': {'_index': 'pylastica_test', '_type': 'bulk_test'}},
            {'name': 'Ringo'}
        ]
        self.assertEqual(expected, data)

        response = bulk.send()

        self.assertIsInstance(response, pylastica.bulk.ResponseSet)
        self.assertTrue(response.is_ok())
        self.assertFalse(response.has_error())
        for i in range(len(response)):
            self.assertIsInstance(response[i], pylastica.bulk.Response)
            self.assertTrue(response[i].is_ok())
            self.assertFalse(response[i].has_error())

        doc_type.index.refresh()
        doc_type2.index.refresh()
        self.assertEqual(3, doc_type.count())
        self.assertEqual(1, doc_type2.count())
        bulk = pylastica.bulk.Bulk(client)
        bulk.add_document(doc3, pylastica.bulk.action.Action.OP_TYPE_DELETE)
        data = bulk.to_list()
        expected = [{'delete': {'_index': 'pylastica_test', '_type': 'bulk_test', '_id': '3'}}]
        self.assertEqual(expected, data)
        bulk.send()
        doc_type.index.refresh()
        self.assertEqual(2, doc_type.count())
        self.assertRaises(pylastica.exception.NotFoundException, doc_type.get_document, 3)
        index.delete()

    def test_update(self):
        index = self._create_index()
        doc_type = index.get_doc_type('bulk_test')
        client = index.client

        doc1 = doc_type.create_document(1, {'name': 'John'})
        doc2 = pylastica.Document(2, {'name': 'Paul'})
        doc3 = doc_type.create_document(3, {'name': 'George'})
        doc4 = doc_type.create_document(data={'name': 'Ringo'})

        doc3.op_type = pylastica.Document.OP_TYPE_CREATE
        documents = [doc1, doc2, doc3, doc4]

        bulk = pylastica.bulk.Bulk(client)
        bulk.doc_type = doc_type
        bulk.add_documents(documents)
        bulk.add_document(pylastica.Document(2, {'name': 'The Walrus'}, doc_type, index), pylastica.bulk.action.Action.OP_TYPE_UPDATE)

        response = bulk.send()
        self.assertIsInstance(response, pylastica.bulk.ResponseSet)
        self.assertTrue(response.is_ok())
        self.assertFalse(response.has_error())
        for i in range(len(response)):
            self.assertIsInstance(response[i], pylastica.bulk.Response)
            self.assertTrue(response[i].is_ok())
            self.assertFalse(response[i].has_error())

        doc_type.index.refresh()

        doc2 = doc_type.get_document('2')
        self.assertEqual('The Walrus', doc2.data['name'])

        #test updating via script
        script = pylastica.Script('ctx._source.name += param1', {'param1': ' was Paul'}, doc_id=2)
        doc2 = pylastica.Document()
        script.upsert = doc2
        action = pylastica.bulk.action.AbstractDocument.create(script, pylastica.bulk.action.AbstractDocument.OP_TYPE_UPDATE)

        bulk = pylastica.bulk.Bulk(client)
        bulk.doc_type = doc_type
        bulk.add_action(action)
        bulk.send()
        index.refresh()

        doc = doc_type.get_document('2')
        self.assertEqual('The Walrus was Paul', doc.data['name'])

        #test upsert
        script = pylastica.Script('ctx._source.counter += count', {'count': 1}, doc_id=5)
        doc = pylastica.Document('', {'counter': 1})
        script.upsert = doc
        action = pylastica.bulk.action.AbstractDocument.create(script, pylastica.bulk.action.AbstractDocument.OP_TYPE_UPDATE)

        bulk = pylastica.bulk.Bulk(client)
        bulk.doc_type = doc_type
        bulk.add_action(action)
        bulk.send()
        index.refresh()

        doc = doc_type.get_document('5')
        self.assertEqual(1, doc.data['counter'])

        #test doc_as_upsert
        doc = pylastica.Document(6, {'test': 'test'})
        doc.doc_as_upsert = True
        update_action = pylastica.bulk.action.AbstractDocument.create(doc, pylastica.bulk.action.AbstractDocument.OP_TYPE_UPDATE)
        bulk = pylastica.bulk.Bulk(client)
        bulk.doc_type = doc_type
        bulk.add_action(update_action)
        response = bulk.send()

        self.assertTrue(response.is_ok())
        self.assertFalse(response.has_error())

        index.refresh()
        doc = doc_type.get_document(6)
        self.assertEqual('test', doc.data['test'])

        index.delete()

if __name__ == '__main__':
    unittest.main()
