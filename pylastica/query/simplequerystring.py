__author__ = 'Joe Linn'

from pylastica.query.abstract import AbstractQuery


class SimpleQueryString(AbstractQuery):
    """
    @see http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/query-dsl-simple-query-string-query.html
    """
    OPERATOR_AND = "and"
    OPERATOR_OR = "or"

    def __init__(self, query, fields=None):
        """
        @param query:
        @type query: str
        @param fields:
        @type fields: list of str
        """
        super(SimpleQueryString, self).__init__()
        self.set_query(query)
        if fields is not None:
            self.set_fields(fields)

    def set_query(self, query):
        """
        Set the querystring for this query
        @param query: see linked documentation for querystring syntax
        @type query: str
        @return:
        @rtype: self
        """
        return self.set_param("query", query)

    def set_fields(self, fields):
        """

        @param fields: the fields on which to perform this query. Defaults to index.query.default_field.
        @type fields: list of str
        @return:
        @rtype: self
        """
        return self.set_param("fields", fields)

    def set_default_operator(self, operator):
        """
        Set the default operator to use if no explicit operator is defined in the query string
        @param operator: see OPERATOR_* constants for options
        @type operator: str
        @return:
        @rtype: self
        """
        return self.set_param("default_operator", operator)

    def set_analyzer(self, analyzer):
        """
        Set the analyzer used to analyze each term of the query
        @param analyzer:
        @type analyzer: str
        @return:
        @rtype: self
        """
        return self.set_param("analyzer", analyzer)