__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter

class Query(AbstractFilter):
    def __init__(self, query=None):
        """

        @param query: query
        @type query: dict or pylastica.query.abstract.AbstractQuery
        """
        super(Query, self).__init__()
        if query is not None:
            self.set_query(query)

    def set_query(self, query):
        """
        Set the query
        @param query:
        @type query: dict or pylastica.query.abstract.AbstractQuery
        @return:
        @rtype: self
        """
        if not isinstance(query, pylastica.query.abstract.AbstractQuery) and not isinstance(query, dict):
            raise TypeError("query must be of type dict or AbstractQuery: %r" % query)
        if isinstance(query, pylastica.query.abstract.AbstractQuery):
            query = query.to_dict()
        self._query = query
        return self

    def _get_base_name(self):
        """

        @return:
        @rtype: str
        """
        if self._params is None or not len(self._params):
            return 'query'
        else:
            return 'fquery'

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        data = super(Query, self).to_dict()
        name = self._get_base_name()
        filter_data = data[name]
        if not filter_data:
            filter_data = self._query
        else:
            filter_data['query'] = self._query
        data[name] = filter_data
        return data

