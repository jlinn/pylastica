__author__ = 'Joe Linn'

import abc

class Searchable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def search(self, query=None, options=None):
        """
        Searches results for a query
        @param query: dict with all query data or a Query object
        @type query: str or dict or pylastica.query.Query
        @param options:
        @type options: dict
        @return: result set with all results
        @rtype: pylastica.resultset.ResultSet
        """
        pass

    @abc.abstractmethod
    def count(self, query=None):
        """
        Counts results for a query. If no query is set, a MatchAll query is used.
        @param query: dict with all query data or a Query object
        @type query: dict or pylastica.query.Query
        @return: number of docs matching the query
        @rtype: int
        """
        pass

    @abc.abstractmethod
    def create_search(self, query=None, options=None):
        """

        @param query:
        @type query: pylastica.query.Query
        @param options:
        @type options:  dict
        @return:
        @rtype: pylastica.search.Search
        """
        pass
