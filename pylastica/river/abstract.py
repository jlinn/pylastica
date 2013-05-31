__author__ = 'Joe Linn'

import abc
import pylastica.param


class AbstractRiver(pylastica.param.Param):
    __metaclass__ = abc.ABCMeta

    river_type = 'river'    #override this in implementing classes

    def __init__(self, client, name, index=None, doc_type=None, bulk_size=100, bulk_timeout='10ms'):
        """
        @param client:
        @type client: pylastica.client.Client
        @param name: name of the river
        @type name: str
        @param index: default index for this river
        @type index: str or pylastica.index.Index
        @param doc_type: default document type for this river
        @type doc_type: str or pylastica.doc_type.DocType
        @param bulk_size: bulk size
        @type bulk_size: int
        @param bulk_timeout: "10ms", for example
        @type bulk_timeout: str
        """
        super(AbstractRiver, self).__init__()
        if self.river_type == 'river':
            raise NotImplementedError("Class property river_type must be overridden in all implementations of AbstractRiver.")
        self._index = {}
        self._params = {}
        self._client = client
        self._name = name
        self.set_index(index).set_doc_type(doc_type).set_bulk_size(bulk_size).set_bulk_timeout(bulk_timeout)

    def set_index(self, index):
        """
        Set the default index for this river
        @param index:
        @type index: str or pylastica.index.Index
        @return:
        @rtype: self
        """
        if isinstance(index, pylastica.index.Index):
            index = index.name
        if isinstance(index, str):
            self._index['name'] = index
        return self

    def set_doc_type(self, doc_type):
        """
        Set the default document type for this river
        @param doc_type:
        @type doc_type: str or pylastica.doc_type.DocType
        @return:
        @rtype: self
        """
        if isinstance(doc_type, pylastica.doc_type.DocType):
            doc_type = doc_type.name
        if isinstance(doc_type, str):
            self._index['type'] = doc_type
        return self

    def set_bulk_size(self, bulk_size):
        """
        Set the bulk size for this river
        @param bulk_size:
        @type bulk_size: int
        @return:
        @rtype: self
        """
        self._index['bulk_size'] = int(bulk_size)
        return self

    def set_bulk_timeout(self, bulk_timeout):
        """
        Set bulk timeout for this river
        @param bulk_timeout: "10ms", for example
        @type bulk_timeout: str
        @return:
        @rtype: self
        """
        self._index['bulk_timeout'] = bulk_timeout
        return self

    def create(self):
        """

        @return:
        @rtype: pylastica.response.Response
        """
        return self._client.request('/_river/%s/_meta' % self._name, pylastica.request.Request.PUT, self.to_dict())

    def delete(self):
        """

        @return:
        @rtype: pylastica.response.Response
        """
        return self._client.request('/_river/%s/' % self._name, pylastica.request.Request.DELETE)

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        return {
            'type': self.river_type,
            self.river_type: self._params,
            'index': self._index
        }
