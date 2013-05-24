__author__ = 'Joe Linn'

from .abstract import AbstractQuery

class MultiMatch(AbstractQuery):
    def set_query(self, query=None):
        """
        Set the query string
        @param query:
        @type query: str
        @return:
        @rtype: self
        """
        if query is None:
            query = ''
        return self.set_param('query', query)

    def set_fields(self, fields=None):
        """
        Set the fields to be used in the query
        @param fields:
        @type fields: list of str
        @return:
        @rtype: self
        """
        if fields is None:
            fields = []
        return self.set_param('fields', fields)

    def set_use_dis_max(self, use_dis_max=True):
        """
        Sets use dis max, indicating to either create a dis_max query or a bool query.
        @param use_dis_max:
        @type use_dis_max: bool
        @return:
        @rtype: self
        """
        return self.set_param('use_dis_max', bool(use_dis_max))

    def set_tie_breaker(self, tie_breaker=0.0):
        """
        Set the tie breaker multiplier value to balance scores between lower and higher scoring fields.
        @param tie_breaker:
        @type tie_breaker: float
        @return:
        @rtype: self
        """
        return self.set_param('tie_breaker', float(tie_breaker))
