__author__ = 'Joe Linn'

import pylastica.response
import pylastica.result

class ResultSet(object):
    def __init__(self, response, query):
        """
        @type response: pylastica.response.Response
        @type query: pylastica.query.Query
        """
        assert isinstance(response, pylastica.response.Response), "response must be of type Response: %r" % response
        assert isinstance(query, pylastica.query.Query), "query must be of type Query: %r" % query
        self._results = []
        self._response = response
        self._query = query
        self._took = 0
        self._timed_out = False
        self._total_hits = 0
        self._max_score = 0
        self._init(response)

    def _init(self, response):
        """
        Loads all data into the results object
        @type response: pylastica.response.Response
        """
        result = response.get_data()
        if 'hits' in result:
            self._total_hits = result['hits']['total'] if 'total' in result['hits'] else 0
            self._max_score = result['hits']['max_score'] if 'max_score' in result['hits'] else 0
            self._took = result['took'] if 'took' in result else 0
            self._timed_out = 'timed_out' in result and result['timed_out'] is not None
            if 'hits' in result['hits']:
                self._results = [pylastica.result.Result(hit) for hit in result['hits']['hits']]

    def get_results(self):
        """
        Returns all results
        @rtype: list
        """
        return self._results

    @property
    def results(self):
        """

        @return:
        @rtype: list of pylastica.result.Result
        """
        return self.get_results()

    def has_facets(self):
        """
        Determine whether or not this result set has facets
        @rtype: bool
        """
        data = self._response.get_data()
        return 'facets' in data

    def get_facets(self):
        """
        Returns all facet results
        @return:
        @rtype: dict
        """
        data = self._response.get_data()
        return data['facets'] if 'facets' in data else {}

    def get_total_hits(self):
        """
        Returns the number of total found hits
        @return:
        @rtype: int
        """
        return int(self._total_hits)

    def get_max_score(self):
        """
        Returns the max score of the results found
        @return:
        @rtype: float
        """
        return float(self._max_score)

    def get_total_time(self):
        """
        Returns the total time taken for this search to complete
        @return: time in milliseconds
        @rtype: int
        """
        return int(self._took)

    def has_timed_out(self):
        """
        Returns true if the query has timed out
        @return:
        @rtype: bool
        """
        return bool(self._timed_out)

    @property
    def response(self):
        """
        Returns the response object
        @return:
        @rtype: pylastica.response.Response
        """
        return self._response

    @property
    def query(self):
        """
        Return the query object
        @return:
        @rtype: pylastica.query.Query
        """
        return self._query

    @property
    def suggests(self):
        """
        Return suggestions
        @return:
        @rtype: dict
        """
        data = self._response.get_data()
        return data['suggest'] if 'suggest' in data else {}

    def has_suggests(self):
        """
        @return: true if this result set contains suggestions
        @rtype: bool
        """
        return 'suggest' in self._response.data

    def __len__(self):
        """
        Returns the size of the current result set
        @return:
        @rtype: int
        """
        return len(self._results)

    def __iter__(self):
        return iter(self._results)

    def __getitem__(self, item):
        """

        @param item:
        @type item: int
        @return:
        @rtype: pylastica.result.Result
        """
        return self._results[item]
