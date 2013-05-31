__author__ = 'Joe Linn'

import pylastica.index


class Percolator(object):

    def __init__(self, index):
        """

        @param index:
        @type index: pylastica.index.Index
        """
        assert isinstance(index, pylastica.index.Index), "index must be an instance of Index: %r" % index
        self._index = index

    def register_query(self, name, query):
        """
        Register a percolator query
        @param name: query name
        @type name: str
        @param query:
        @type query: str or pylastica.query.Query or pylastica.query.AbstractQuery
        @return:
        @rtype: pylastica.response.Response
        """
        path = '_percolator/%s/%s' % (self._index.name, name)
        query = pylastica.query.Query.create(query)
        return self._index.client.request(path, pylastica.request.Request.PUT, query.to_dict())

    def unregister_query(self, name):
        """
        Remove a percolator query
        @param name: name of the query
        @type name: str
        @return:
        @rtype: pylastica.response.Response
        """
        path = '_percolator/%s/%s' % (self._index.name, name)
        return self._index.client.request(path, pylastica.request.Request.DELETE)

    def match_doc(self, doc, query=None):
        """
        Match a document to percolator queries
        @param doc:
        @type doc: pylastica.document.Document
        @param query:
        @type query: str or pylastica.query.Query or pylastica.query.AbstractQuery
        @return:
        @rtype: pylastica.response.Response
        """
        path = "%s/type/_percolate" % self._index.name
        data = {'doc': doc.data}
        if query is not None:
            query = pylastica.query.Query.create(query)
            data['query'] = query.query
        response = self._index.client.request(path, data=data)
        data = response.data
        return data['matches']

    @property
    def index(self):
        """

        @return:
        @rtype: pylastica.index.Index
        """
        return self._index
