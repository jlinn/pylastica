__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class MappingTest(unittest.TestCase, Base):
    def test_mapping_store_fields(self):
        index = self._create_index('test')
        doc_type = index.get_doc_type('test')

        mapping = pylastica.doc_type.Mapping(doc_type, {
            'firstname': {'type': 'string', 'store': 'yes'},
            'lastname': {'type': 'string'}
        })
        mapping.disable_source()

        doc_type.set_mapping(mapping)

        firstname = 'Joe'
        doc_type.add_document(pylastica.Document(1, {'firstname': firstname, 'lastname': 'Linn'}))
        index.refresh()

        query_string = pylastica.query.QueryString('linn')
        query = pylastica.query.Query.create(query_string)
        query.set_fields(['*'])

        result_set = doc_type.search(query)
        result = result_set[0]
        fields = result.get_fields()

        self.assertEqual(firstname, fields['firstname'][0])
        self.assertFalse('lastname' in fields)
        self.assertEqual(1, len(fields))

        index.flush()
        document = doc_type.get_document('1')
        self.assertEqual(0, len(document.data))
        index.delete()

    def test_enable_all_field(self):
        index = self._create_index()
        doc_type = index.get_doc_type('test')
        mapping = pylastica.doc_type.Mapping(doc_type)
        mapping.enable_all_field()

        data = mapping.to_dict()
        self.assertTrue(data[doc_type.name]['_all']['enabled'])
        response = mapping.send()
        self.assertTrue(response.is_ok())
        index.delete()

    def test_set_meta(self):
        index = self._create_index()
        doc_type = index.get_doc_type('test')
        mapping = pylastica.doc_type.Mapping(doc_type, {
            'firstname': {'type': 'string', 'store': 'yes'},
            'lastname': {'type': 'string'}
        })
        mapping.set_meta({
            'class': 'test'
        })
        doc_type.set_mapping(mapping)

        mapping_data = doc_type.mapping
        self.assertEqual('test', mapping_data['pylastica_test']['mappings']['test']['_meta']['class'])
        index.delete()


if __name__ == '__main__':
    unittest.main()
