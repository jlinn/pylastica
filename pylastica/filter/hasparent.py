__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter
import pylastica.query

class HasParent(AbstractFilter):
    def __init__(self, query, doc_type):
        """

        @param query: query
        @type query: str or pylastica.query.Query or pylastica.query.abstract.AbstractQuery
        @param doc_type: parent document type
        @type doc_type: str
        """
        super(HasParent, self).__init__()
        self.set_query(query)
        self.set_doc_type(doc_type)

    def set_query(self, query):
        """
        Set the query object
        @param query: query
        @type query: str or pylastica.query.Query or pylastica.query.abstract.AbstractQuery
        @return:
        @rtype: self
        """
        query = pylastica.query.Query.create(query)
        data = query.to_dict()
        return self.set_param('query', data['query'])

    def set_doc_type(self, doc_type):
        """
        Set the type of the parent document
        @param doc_type: parent doc type
        @type doc_type: str
        @return:
        @rtype: self
        """
        return self.set_param('type', doc_type)

    def set_scope(self, scope):
        """
        Set the scope
        @param scope:
        @type scope: str
        @return:
        @rtype: self
        """
        return self.set_param('_scope', scope)
