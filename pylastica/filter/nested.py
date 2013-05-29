__author__ = 'Joe Linn'

from .abstractfilter import AbstractFilter
import pylastica.query.abstract


class Nested(AbstractFilter):
    SCORE_MODE_AVG = 'avg'
    SCORE_MODE_TOTAL = 'total'
    SCORE_MODE_MAX = 'max'
    SCORE_MODE_NONE = 'none'

    def set_path(self, path):
        """
        Set the nested document path
        @param path: document path
        @type path: str
        @return:
        @rtype: self
        """
        return self.set_param('path', path)

    def set_query(self, query):
        """
        Set the nested query
        @param query: query object
        @type query: pylastica.query.abstract.AbstractQuery
        @return:
        @rtype: self
        """
        if not isinstance(query, pylastica.query.abstract.AbstractQuery):
            raise TypeError("query must be of type AbstractQuery: %r" % query)
        return self.set_param('query', query.to_dict())

    def set_score_mode(self, mode):
        """
        Set the score mode
        @param mode: see SCORE_MODE_* class properties for options
        @type mode: str
        @return:
        @rtype: self
        """
        return self.set_param('score_mode', mode)
