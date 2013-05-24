__author__ = 'Joe Linn'

from .abstract import AbstractQuery

class Match(AbstractQuery):
    def set_field(self, field, values):
        """
        Set the param for the message array
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
        @param field: field name
        @type field: str
        @param key:
        @type key: str
        @param value:
        @type value: mixed
        @return:
        @rtype: self
        """
        if field not in self._params:
            self._params[field] = {}
        self._params[field][key] = value
        return self

    def set_field_query(self, field, query):
        """
        Set the query string for a field
        @param field:
        @type field: str
        @param query:
        @type query: str
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'query', query)

    def set_field_type(self, field, doc_type):
        """
        Set the doc type for a field
        @param field:
        @type field: str
        @param doc_type:
        @type doc_type: str
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'type', doc_type)

    def set_field_operator(self, field, operator):
        """
        Set the field operator
        @param field:
        @type field: str
        @param operator:
        @type operator: str
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'operator', operator)

    def set_field_analyzer(self, field, analyzer):
        """
        Set the field analyzer
        @param field:
        @type field: str
        @param analyzer:
        @type analyzer: str
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'anaylzer', analyzer)

    def set_field_boost(self, field, boost=1.0):
        """
        Set the boost for a field
        @param field:
        @type field: str
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'boost', float(boost))

    def set_field_minimum_should_match(self, field, minimum):
        """
        Set the filed minimum should match
        @param field:
        @type field: str
        @param minimum:
        @type minimum: int
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'minimum_should_match', int(minimum))

    def set_field_fuzziness(self, field, fuzziness):
        """
        Set field fuzziness
        @param field:
        @type field: str
        @param fuzziness:
        @type fuzziness: float
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'fuzziness', float(fuzziness))

    def set_field_fuzzy_rewrite(self, field, fuzzy_rewrite):
        """
        Set field fuzzy rewrite
        @param field:
        @type field: str
        @param fuzzy_rewrite:
        @type fuzzy_rewrite: str
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'fuzzy_rewrite', fuzzy_rewrite)

    def set_field_prefix_length(self, field, prefix_length):
        """
        Set field prefix length
        @param field:
        @type field: str
        @param prefix_length:
        @type prefix_length: int
        @return:
        @rtype: self
        """
        return self.set_field_param(field, 'prefix_length', int(prefix_length))

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
        return self.set_field_param(field, 'max_expansions', int(max_expansions))
