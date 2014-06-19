__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class ScriptFieldsTest(unittest.TestCase, Base):
    def setUp(self):
        self._index = self._create_index()

    def tearDown(self):
        self._index.delete()

    def test_query(self):
        doc_type = self._index.get_doc_type('test')
        doc_type.add_document(pylastica.Document(1, {'firstname': 'nicolas', 'lastname': 'ruflin'}))
        self._index.refresh()

        query = pylastica.query.Query()
        script = pylastica.Script('1 + 2')
        script_fields = pylastica.ScriptFields({
            'test': script
        })
        query.set_script_fields(script_fields)
        result_set = doc_type.search(query)
        first = result_set[0].get_data()

        self.assertEqual(3, first['test'][0])


if __name__ == '__main__':
    unittest.main()
