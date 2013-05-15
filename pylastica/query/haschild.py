__author__ = 'Joe Linn'

from . import abstract

class HasChild(abstract.AbstractQuery):
    def __init__(self, query, doc_type=None):
        """

        @param query:
        @type query: str or pylastica.query.Query or pylastica.query.abstract.AbstractQuery
        @param doc_type: child document type
        @type doc_type: str
        """
        super(HasChild, self).__init__()
        self.set_query(query)
        self.set_type(doc_type)

    def set_query(self, query):
        """
        Set the query object
        @param query:
        @type query: str or pylastica.query.Query or pylastica.query.abstract.AbstractQuery
        @return:
        @rtype: self
        """
        import pylastica.query
        query = pylastica.query.Query.create(query)
        data = query.to_dict()
        return self.set_param('query', data['query'])

    def set_type(self, doc_type):
        """
        Set the child document type
        @param doc_type:
        @type doc_type: str
        @return:
        @rtype: self
        """
        return self.set_param('type', doc_type)

    def set_scope(self, scope):
        """
        Set the scope of the query
        @param scope:
        @type scope: str
        @return:
        @rtype: self
        """
        return self.set_param('_scope', scope)
