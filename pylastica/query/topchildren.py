__author__ = 'Joe Linn'

import pylastica

class TopChildren(pylastica.query.AbstractQuery):
    def __init__(self, query, doc_type=None):
        """

        @param query: query string or query object
        @type query: str or pylastica.query.Query or pylastica.query.AbstractQuery
        @param doc_type: parent document type
        @type doc_type: str
        """
        self.set_query(query)
        self.set_type(doc_type)

    def set_query(self, query):
        """
        Set the query
        @param query:
        @type query: str or pylastica.query.Query or pylastica.query.AbstractQuery
        @return:
        @rtype: self
        """
        query = pylastica.query.Query.create(query)
        return self.set_param('query', query.to_dict()['query'])

    def set_type(self, doc_type):
        """
        Set the parent document type
        @param doc_type:
        @type doc_type: str
        @return:
        @rtype: self
        """
        return self.set_param('type', doc_type)
