__author__ = 'Joe Linn'

import os
import unittest
import pylastica
from ..base import Base


class IndexTest(unittest.TestCase, Base):
    def setUp(self):
        self._data_path = '/'.join(os.path.abspath(__file__).split('/')[:-1]) + '/../../test_data/'
        client = self._get_client()
        node = client.cluster.nodes[0]
        self._has_attachment_plugin = node.info.has_plugin('mapper-attachments')

    def test_mapping(self):
        index = self._create_index()
        doc = pylastica.Document(1, {
            'id': 1,
            'email': 'test@test.com',
            'username': 'jlinn',
            'test': ['2', '3', '5']
        })
        doc_type = index.get_doc_type('test')
        mapping = {
            'id': {'type': 'integer', 'store': True},
            'email': {'type': 'string', 'store': 'no'},
            'username': {'type': 'string', 'store': 'no'},
            'test': {'type': 'integer', 'store': 'no'}
        }
        doc_type.mapping = mapping
        doc_type.add_document(doc)
        index.optimize()
        stored_mapping = doc_type.mapping
        self.assertEqual(stored_mapping['test']['properties']['id']['type'], 'integer')
        self.assertTrue(stored_mapping['test']['properties']['id']['store'])
        index.delete()

    def test_parent(self):
        index = self._create_index()
        type_blog = pylastica.doc_type.DocType(index, 'blog')
        type_comment = pylastica.doc_type.DocType(index, 'comment')
        mapping = pylastica.doc_type.Mapping()
        mapping.set_param('_parent', {'type': 'blog'})
        type_comment.mapping = mapping
        entry_1 = pylastica.Document(1)
        entry_1.set('title', "Hello world!")
        type_blog.add_document(entry_1)
        entry_2 = pylastica.Document(2)
        entry_2.set('title', 'Foo bar')
        type_blog.add_document(entry_2)
        entry_3 = pylastica.Document(3)
        entry_3.set('title', 'Till dawn')
        type_blog.add_document(entry_3)
        comment = pylastica.Document(1)
        comment.set('author', 'Max')
        comment.parent = 2
        type_comment.add_document(comment)
        index.optimize()
        query = pylastica.query.HasChild('Max', 'comment')
        result_set = type_blog.search(query)
        self.assertEqual(1, len(result_set))
        self.assertEqual({'title': 'Foo bar'}, result_set[0].data)
        index.delete()

    def test_add_pdf_file(self):
        if not self._has_attachment_plugin:
            self.skipTest('Plugin mapper-attachments is not installed.')
        index_mapping = {
            'file': {'type': 'attachment', 'store': 'no'},
            'text': {'type': 'string', 'store': 'no'}
        }
        index_params = {'index': {'number_of_shards': 1, 'number_of_replicas': 0}}
        index = self._create_index()
        doc_type = pylastica.doc_type.DocType(index, 'test')
        index.create(index_params, True)
        doc_type.mapping = index_mapping

        doc_1 = pylastica.Document(1)
        doc_1.add_file('file', self._data_path + 'test.pdf', 'application/pdf')
        doc_1.set('text', 'base1 world')
        doc_type.add_document(doc_1)

        doc_2 = pylastica.Document(2)
        doc_2.set('text', 'running in base1')
        doc_type.add_document(doc_2)

        index.optimize()

        result_set = doc_type.search('xodoa')
        self.assertEqual(1, len(result_set))
        result_set = doc_type.search('base1')
        self.assertEqual(2, len(result_set))
        result_set = doc_type.search('ruflin')
        self.assertEqual(1, len(result_set))
        result_set = doc_type.search('owef')
        self.assertEqual(0, len(result_set))
        index.delete()

    def test_add_pdf_file_content(self):
        if not self._has_attachment_plugin:
            self.skipTest('Plugin mapper-attachments is not installed.')
        index_mapping = {
            'file': {'type': 'attachment', 'store': 'no'},
            'text': {'type': 'string', 'store': 'no'}
        }
        index_params = {'index': {'number_of_shards': 1, 'number_of_replicas': 0}}
        index = self._create_index()
        doc_type = pylastica.doc_type.DocType(index, 'test')
        index.create(index_params, True)
        doc_type.mapping = index_mapping

        doc_1 = pylastica.Document(1)
        doc_1.add_file_content('file', open(self._data_path + 'test.pdf', 'rb').read())
        doc_1.set('text', 'base1 world')
        doc_type.add_document(doc_1)

        doc_2 = pylastica.Document(2)
        doc_2.set('text', 'running in base1')
        doc_type.add_document(doc_2)

        index.optimize()
        result_set = doc_type.search('xodoa')
        self.assertEqual(1, len(result_set))
        result_set = doc_type.search('base1')
        self.assertEqual(2, len(result_set))
        result_set = doc_type.search('ruflin')
        self.assertEqual(1, len(result_set))
        result_set = doc_type.search('owef')
        self.assertEqual(0, len(result_set))
        index.delete()

    def test_add_remove_alias(self):
        client = self._get_client()
        index_name_1 = 'test1'
        alias_name = 'test-alias'
        type_name = 'test'
        index = client.get_index(index_name_1)
        index.create({'index': {'number_of_shards': 1, 'number_of_replicas': 0}}, True)
        doc = pylastica.Document(1, {'id': 1, 'email': 'test@test.com', 'username': 'ruflin'})
        doc_type = index.get_doc_type(type_name)
        doc_type.add_document(doc)
        index.refresh()
        result_set = doc_type.search('ruflin')
        self.assertEqual(1, len(result_set))
        data = index.add_alias(alias_name, True).data
        self.assertTrue(data['ok'])
        index_2 = client.get_index(alias_name)
        type_2 = index_2.get_doc_type(type_name)
        result_set_2 = type_2.search('ruflin')
        self.assertEqual(1, len(result_set_2))
        response = index.remove_alias(alias_name).data
        self.assertTrue(response['ok'])
        index.delete()

