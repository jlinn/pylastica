__author__ = 'Joe Linn'

import unittest
import pylastica
from tests.base import Base


class HttpTest(unittest.TestCase, Base):
    def get_config(self):
        return [
            [
                {'transport': 'Http', 'host': self._get_hosts()[0]['host']},
                'GET'
            ],
            [
                {'transport': {'type': 'Http', 'postWithRequestBody': False}, 'host': self._get_hosts()[0]['host']},
                'GET'
            ],
            [
                {'transport': {'type': 'Http', 'postWithRequestBody': True}, 'host': self._get_hosts()[0]['host']},
                'POST'
            ]
        ]

    def test_dynamic_http_method_based_on_config_parameter(self):
        for test_data in self.get_config():
            http_method = test_data[1]
            config = test_data[0]
            client = pylastica.Client(**config)

            index = client.get_index('dynamic_http_method_test')
            index.create(options=True)

            doc_type = index.get_doc_type('test')
            doc_type.add_document(pylastica.Document(1, {'test': 'test'}))
            index.refresh()

            result_set = index.search('test')

            self.assertTrue('test' in result_set[0].data)
            index.delete()


if __name__ == '__main__':
    unittest.main()
