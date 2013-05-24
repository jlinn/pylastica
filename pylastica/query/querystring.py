__author__ = 'Joe Linn'

from .abstract import AbstractQuery


class QueryString(AbstractQuery):
    def __init__(self, query_string=''):
        """
        @param query_string: optional query string
        @type query_string: str
        """
        super(QueryString, self).__init__()
        self.set_query(query_string)

    def set_query(self, query):
        """
        Sets a new query string for the object
        @param query:
        @type query: str
        @return:
        @rtype: self
        """
        assert isinstance(query, str), "query must be a str: %r" % query
        self._query_string = query
        return self

    def set_default_field(self, field):
        """
        Set the default field
        @param field: field name
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param('default_field', field)

    def set_default_operator(self, operator):
        """
        Set the default operator
        @param operator: AND or OR
        @type operator: str
        @return:
        @rtype: self
        """
        return self.set_param('default_operator', operator)

    def set_analyzeer(self, analyzer):
        """
        Sets the analyzer for this query
        @param analyzer:
        @type analyzer: str
        @return:
        @rtype: self
        """
        return self.set_param('analyzer', analyzer)

    def set_allow_leading_wildcard(self, allow=True):
        """
        Sets the parameter to allow * and ? as first characters
        @param allow:
        @type allow: bool
        @return:
        @rtype: self
        """
        return self.set_param('allow_leading_wildcard', bool(allow))

    def set_lowercase_expanded_terms(self, lowercase=True):
        """
        Sets the parameter to auto-lowercase terms of queries
        @param lowercase:
        @type lowercase: bool
        @return:
        @rtype: self
        """
        return self.set_param('lowercase_expanded_terms', bool(lowercase))

    def set_enable_position_increments(self, enabled=True):
        """
        Enable or disable position increments in result queries
        @param enabled:
        @type enabled: bool
        @return:
        @rtype: self
        """
        return self.set_param('enable_position_incremends', bool(enabled))

    def set_fuzzy_prefix_length(self, length=0):
        """
        Set the fuzzy prefix length parameter
        @param length:
        @type length: int
        @return:
        @rtype: self
        """
        return self.set_param('fuzzy_prefix_length', int(length))

    def set_phrase_stop(self, phrase_stop=0):
        """
        Set the phrase stop. If 0, exact phrases are required.
        @param phrase_stop:
        @type phrase_stop: int
        @return:
        @rtype: self
        """
        return self.set_param('phrase_stop', int(phrase_stop))

    def set_boost(self, boost=1.0):
        """
        Set the boost for the query
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        return self.set_param('boost', float(boost))

    def set_analyze_wildcard(self, analyze=True):
        """
        Allows analysis of wildcard terms
        @param analyze:
        @type analyze: bool
        @return:
        @rtype: self
        """
        return self.set_param('analyze_wildcard', bool(analyze))

    def set_auto_generate_phrase_queries(self, auto=True):
        """
        Automatically generate phrase queries
        @param auto:
        @type auto: bool
        @return:
        @rtype: self
        """
        return self.set_param('auto_generate_phrase_queries', bool(auto))

    def set_fields(self, fields):
        """
        Set the fields. If no fields are set, _all is used.
        @param fields:
        @type fields: list of str
        @return:
        @rtype: self
        """
        assert isinstance(fields, list), "fields must be a list: %r" % fields
        return self.set_param('fields', fields)

    def set_use_dis_max(self, value=True):
        """
        Set whether or not to use bool or dis_max queries to internally combine results for multi field search
        @param value:
        @type value: bool
        @return:
        @rtype: self
        """
        return self.set_param('use_dis_max', bool(value))

    def set_tie_breaker(self, tie_breaker=0):
        """
        When using dis_max, the disjunction max tie breaker
        @param tie_breaker:
        @type tie_breaker: int
        @return:
        @rtype: self
        """
        return self.set_param('tie_breaker', int(tie_breaker))

    def set_rewrite(self, rewrite=None):
        """
        Set the rewrite condition
        @param rewrite:
        @type rewrite: str
        @return:
        @rtype: self
        """
        if rewrite is None:
            rewrite = ''
        return self.set_param('rewrite', rewrite)

    def to_dict(self):
        dictionary = {'query': self._query_string}
        dictionary.update(self.params)
        return {
            'query_string': dictionary
        }

