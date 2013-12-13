from pylastica.suggest.abstract import AbstractSuggestion

__author__ = 'Joe Linn'

import pylastica.param
import pylastica.scriptfields
from .abstract import AbstractQuery
from .matchall import MatchAll
from pylastica.suggest.suggest import Suggest


class Query(pylastica.param.Param):
    def __init__(self, query=None):
        """

        @param query: optional query object
        @type query: dict or pylastica.query.AbstractQuery or Suggest
        """
        super(Query, self).__init__()
        if isinstance(query, dict):
            self.set_raw_query(query)
        elif isinstance(query, AbstractQuery):
            self.query = query
        elif isinstance(query, Suggest):
            self.set_suggest(query)

    @classmethod
    def create(cls, query):
        """
        Transforms a string or dict into a Query object
        @param cls:
        @type cls:
        @param query:
        @type query: mixed
        @return:
        @rtype: cls
        """
        if isinstance(query, Query):
            return query
        elif isinstance(query, AbstractQuery) or isinstance(query, Suggest):
            return cls(query)
        elif isinstance(query, AbstractSuggestion):
            return cls(Suggest(query))
        elif isinstance(query, pylastica.filter.AbstractFilter):
            new_query = cls()
            new_query.set_filter(query)
            return new_query
        elif query is None or query == '':
            return cls(MatchAll())
        elif isinstance(query, str):
            from .querystring import QueryString
            return cls(QueryString(query))
        raise NotImplementedError()

    def set_raw_query(self, query):
        """
        Sets query as a raw dict. Will overwrite all currently set arguments
        @param query:
        @type query: dict
        @return:
        @rtype: self
        """
        assert isinstance(query, dict), "query must be a dict: %r" % query
        self._params = query
        return self

    @property
    def query(self):
        """
        Get the query dictionary
        @return:
        @rtype: dict
        """
        return self.get_param('query')

    @query.setter
    def query(self, query):
        """
        Set the query
        @param query:
        @type query: AbstractQuery
        """
        assert isinstance(query, AbstractQuery), "query must be instance of AbstractQuery: %r" % query
        self.set_param('query', query.to_dict())

    def set_filter(self, filter):
        """
        Set the filter for this query
        @param filter:
        @type filter: pylastica.filter.AbstractFilter
        @return:
        @rtype: self
        """
        assert isinstance(filter, pylastica.filter.AbstractFilter), "filter must be an instance of an implementation of AbstractFilter: %r" % filter
        return self.set_param('filter', filter.to_dict())

    def set_from(self, start_from):
        """
        Sets the start from which the search results should be returned
        @param start_from:
        @type start_from: int
        @return:
        @rtype: self
        """
        return self.set_param('from', int(start_from))

    def set_sort(self, sort_args):
        """
        Sets sort arguments for the query. Replaces existing values.
        @see: http://www.elasticsearch.org/guide/reference/api/search/sort.html
        @param sort_args:
        @type sort_args: dict
        @return:
        @rtype: self
        """
        return self.set_param('sort', sort_args)

    def add_sort(self, sort):
        """
        Adds a sort param to the query
        @param sort:
        @type sort: mixed
        @return:
        @rtype: self
        """
        return self.add_param('sort', sort)

    def set_highlight(self, highlight_args):
        """
        Sets highlight arguments for the query
        @param highlight_args:
        @type highlight_args: dict
        @return:
        @rtype: self
        """
        return self.set_param('highlight', highlight_args)

    def add_highlight(self, highlight):
        """
        Adds a highlight argument
        @param highlight:
        @type highlight: mixed
        @return:
        @rtype: self
        """
        return self.add_param('highlight', highlight)

    def set_size(self, size=10):
        """
        Set the maximum number of results for this query
        @param size:
        @type size: int
        @return:
        @rtype: self
        """
        return self.set_param('size', int(size))

    def set_explain(self, explain=True):
        """
        Enables explain on the query
        @param explain:
        @type explain: bool
        @return:
        @rtype: self
        """
        return self.set_param('explain', bool(explain))

    def set_version(self, version=True):
        """
        Enables version on the query
        @param version:
        @type version: bool
        @return:
        @rtype: self
        """
        return self.set_param('version', bool(version))

    def set_fields(self, fields):
        """
        Sets the fields to be returned by the query
        @param fields: list of field names
        @type fields: list of str
        @return:
        @rtype: self
        """
        return self.set_param('fields', fields)

    def set_script_fields(self, script_fields):
        """
        Set script fields
        @param script_fields:
        @type script_fields: dict or pylastica.scriptfields.ScriptFields
        @return:
        @rtype: self
        """
        if isinstance(script_fields, dict):
            script_fields = pylastica.scriptfields.ScriptFields(script_fields)
        return self.set_param('script_fields', script_fields.to_dict())

    def add_script_field(self, name, script):
        """
        Add a script to the query
        @param name: name of the script
        @type name: str
        @param script:
        @type script: pylastica.script.Script
        @return:
        @rtype: self
        """
        assert isinstance(script, pylastica.script.Script), "script must be an instance of Script: %r" % script
        self._params['script_fields'][name] = script.to_dict()
        return self

    def set_facets(self, facets):
        """
        Sets all facets for this query object. Replaces existing facets
        @param facets:
        @type facets: dict of pylastica.facet.AbstractFacet
        @return:
        @rtype: self
        """
        self._params['facets'] = {}
        for facet in facets:
            self.add_facet(facet)
        return self

    def add_facet(self, facet):
        """
        Add a facet to the query
        @param facet:
        @type facet: pylastica.facet.AbstractFacet
        @return:
        @rtype: self
        """
        assert isinstance(facet, pylastica.facet.AbstractFacet), "facet must be an instance of an implementation of AbstractFacet: %r" % facet
        if 'facets' not in self._params:
            self._params['facets'] = {}
        self._params['facets'][facet.name] = facet.to_dict()
        return self

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        #if no query is set, all query is chosen by default
        if 'query' not in self._params:
            self.query = pylastica.query.MatchAll()
        return self._params

    def set_min_score(self, min_score):
        """
        Allows filtering of documents based on a minimum score
        @param min_score:
        @type min_score: float
        @return:
        @rtype: self
        """
        assert isinstance(min_score, int) or isinstance(min_score, float), "min_score must be either a float or int: %r" % min_score
        return self.set_param('min_score', min_score)

    def set_suggest(self, suggest):
        """

        @param suggest:
        @type suggest: pylastica.suggest.Suggest
        @return:
        @rtype: self
        """
        self._params.update(suggest.to_dict())
        return self
