__author__ = 'Joe Linn'

from .abstract import AbstractQuery


class Nested(AbstractQuery):
    SCORE_MODE_AVG = 'avg'
    SCORE_MODE_TOTAL = 'total'
    SCORE_MODE_MAX = 'max'
    SCORE_MODE_NONE = 'none'

    def set_path(self, path):
        """
        Set the path for the nested query
        @param path:
        @type path: str
        @return:
        @rtype: eslf
        """
        return self.set_param('path', path)

    def set_query(self, query):
        """
        Set the query for this nested query
        @param query:
        @type query: pylastica.query.AbstractQuery
        @return:
        @rtype: self
        """
        assert isinstance(query, AbstractQuery), "query must be an instance of an implementation of AbstractQuery: %r" % query
        return self.set_param('query', query.to_dict())

    def set_score_mode(self, mode):
        """
        Set score method
        @param mode: options: avg, total, max, none
        @type mode: str
        @return:
        @rtype: self
        """
        return self.set_param('score_mode', mode)
