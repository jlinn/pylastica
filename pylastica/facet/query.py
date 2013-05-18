__author__ = 'Joe Linn'

from .abstractfacet import AbstractFacet
import pylastica.query.abstract


class Query(AbstractFacet):
    def set_query(self, query):
        """
        Set the query for this facet
        @param query:
        @type query: pylastica.query.abstract.AbstractQuery
        @return:
        @rtype: self
        """
        if not isinstance(query, pylastica.query.abstract.AbstractQuery):
            raise TypeError("query must be an instance of AbstractQuery: %r" % query)
        return self._set_facet_param('query', query.to_dict())
