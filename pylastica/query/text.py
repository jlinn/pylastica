__author__ = 'Joe Linn'

from .abstract import AbstractQuery


class Text(AbstractQuery):
    def set_field(self, field, values):
        """
        Set the field for this query
        @param field:
        @type field: str
        @param values:
        @type values: mixed
        @return:
        @rtype: self
        """
        return self.set_param(field, values)

    def set_field_param(self, field, key, value):
        """
        Set a param for the given field
        @param field:
        @type field: str
        @param key:
        @type key: str
        @param value:
        @type value: str or int
        @return:
        @rtype: self
        """
        if field not in self._params:
            self._params[field] = {}
        self._params[field][key] = value
        return self

    def set_field_query(self, field, query):
        """
        Set the query string for the given field
        @param field:
        @type field: str
        @param query:
        @type query: str
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'query', query)

    def set_field_type(self, field, query_type):
        """
        Set the query type for the field
        @param field:
        @type field: str
        @param query_type: text query type
        @type query_type: str
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'type', query_type)

    def set_field_max_expansions(self, field, max_expansions):
        """
        Set field max expansions
        @param field:
        @type field: str
        @param max_expansions:
        @type max_expansions: int
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'max_expansions', max_expansions)
