__author__ = 'Joe Linn'

from .abstract import AbstractQuery


class Simple(AbstractQuery):
    def __init__(self, query):
        """
        Constructs a query from a dict
        @param query:
        @type query: dict
        """
        super(Simple, self).__init__()
        self.set_query(query)

    def set_query(self, query):
        """
        Set a new query dict
        @param query:
        @type query: dict
        @return:
        @rtype: self
        """
        self._query = query
        return self

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        return self._query
