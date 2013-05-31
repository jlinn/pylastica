__author__ = 'Joe Linn'

import unittest
import pylastica
from .base import Base

class TestDocument(unittest.TestCase, Base):
    def test_add_file(self):
        doc = pylastica.Document()
        return_value = doc.add_file('key', '/dev/null')
        self.assertIsInstance(return_value, pylastica.Document)

    def test_add_geo_point(self):
        doc = pylastica.Document()
        return_value = doc.add_geopoint('point', 37.789625,-122.395427)
        self.assertIsInstance(return_value, pylastica.Document)

    def test_set_data(self):
        doc = pylastica.Document()
        return_value = doc.set_data({'data': 5})
        self.assertIsInstance(return_value, pylastica.Document)

    def test_to_dict(self):
        doc_id = '17'
        data = {'hello': 'world'}
        doc_type = 'testtype'
        index = 'testindex'
        doc = pylastica.Document(doc_id, data, doc_type, index)
        result = {'_index': index, '_type': doc_type, '_id': doc_id, '_source': data}
        self.assertEqual(result, doc.to_dict())

    def test_set_doc_type(self):
        doc = pylastica.Document()
        doc.doc_type = 'type'
        self.assertEqual('type', doc.doc_type)
        index = pylastica.index.Index(self._get_client(), 'index')
        doc_type = index.get_doc_type('type')
        doc.index = 'index2'
        self.assertEqual('index2', doc.index)
        doc.doc_type = doc_type
        self.assertEqual('index', doc.index)
        self.assertEqual('type', doc.doc_type)

    def test_set_index(self):
        doc = pylastica.Document()
        doc.index = 'index2'
        doc.doc_type = 'type2'
        self.assertEqual('index2', doc.index)
        self.assertEqual('type2', doc.doc_type)
        index = pylastica.index.Index(self._get_client(), 'index')
        doc.index = index
        self.assertEqual('index', doc.index)
        self.assertEqual('type2', doc.doc_type)

    def test_has_id(self):
        doc = pylastica.Document()
        self.assertFalse(doc.has_id())
        doc.doc_id = ''
        self.assertFalse(doc.has_id())
        doc.doc_id = 0
        self.assertTrue(doc.has_id())
        doc.doc_id = 'hello'
        self.assertTrue(doc.has_id())

    def test_set_script(self):
        doc = pylastica.Document()
        script = pylastica.Script('ctx._source.counter += count')
        script.set_param('count', 1)
        self.assertFalse(doc.has_script())
        doc.script = script
        self.assertTrue(doc.has_script())
        self.assertEqual(script, doc.script)

if __name__ == '__main__':
    unittest.main()
