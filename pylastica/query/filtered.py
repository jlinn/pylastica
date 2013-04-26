__author__ = 'Joe Linn'

import pylastica

class Filtered(pylastica.query.AbstractQuery):
    def __init__(self, query, filter):
        """

        @param query:
        @type query: pylastica.query.AbstractQuery
        @param filter:
        @type filter: pylastica.filter.AbstractFilter
        """
        self.query = query
        self.filter = filter

    @property
    def query(self):
        """

        @return:
        @rtype: pylastica.query.AbstractQuery
        """
        return self._query

    @query.setter
    def query(self, query):
        """

        @param query:
        @type query: pylastica.query.AbstractQuery
        """
        assert isinstance(query, pylastica.query.AbstractQuery), "query must be instance of implementation of AbstractQuery: %r" % query
        self._query = query

    @property
    def filter(self):
        """

        @return:
        @rtype: pylastica.filter.AbstractFilter
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """

        @param filter:
        @type filter: pylastica.filter.AbstractFilter
        """
        assert isinstance(filter, pylastica.filter.AbstractFilter), "filter must be instance of implementation of AbstractFilter: %r" % filter
        self._filter = filter

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        return {
            'query': self.query.to_dict(),
            'filter': self.filter.to_dict()
        }
