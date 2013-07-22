__author__ = 'Joe Linn'

from .abstract import AbstractQuery


class Common(AbstractQuery):
    OPERATOR_AND = 'and'
    OPERATOR_OR = 'or'

    def __init__(self, field, query, cutoff_frequency):
        """
        @param field: The field on which to query
        @type field: str
        @param query: The query string
        @type query: str
        @param cutoff_frequency: percentage in decimal form (.001 == 0.1%)
        @type cutoff_frequency: float
        """
        super(Common, self).__init__()
        self._query_params = {}
        self.set_field(field)
        self.set_query(query)
        self.set_cutoff_frequency(cutoff_frequency)

    def set_field(self, field):
        """
        Set the field on which to query
        @param field: The field on which to query
        @type field: str
        @return:
        @rtype: self
        """
        self._field = field
        return self

    def set_query(self, query):
        """
        Set the query string for this query
        @param query: the query string
        @type query: str
        @return:
        @rtype: self
        """
        return self.set_query_param('query', query)

    def set_cutoff_frequency(self, frequency):
        """
        Set the frequency below which terms will be put in the low frequency group
        @param frequency: percentage in decimal form (.001 == 0.1%)
        @type frequency: float
        @return:
        @rtype: self
        """
        return self.set_query_param('cutoff_frequency', float(frequency))

    def set_low_frequency_operator(self, operator):
        """
        Set the logic operator for low frequency terms
        @param operator: See OPERATOR_* attributes for options.
        @type operator: str
        @return:
        @rtype: self
        """
        return self.set_query_param('low_freq_operator', operator)

    def set_high_frequency_operator(self, operator):
        """
        Set the logic operator for high frequency terms
        @param operator: See OPERATOR_* attributes for options.
        @type operator: str
        @return:
        @rtype: self
        """
        return self.set_query_param('high_freq_operator', operator)

    def set_minimum_should_match(self, minimum):
        """
        Specify the minimum number of low frequency terms which must be present
        @param minimum: minimum number of low frequency terms which must be present
        @type minimum: int
        @return:
        @rtype: self
        """
        return self.set_query_param('minimum_should_match', minimum)

    def set_boost(self, boost):
        """
        Set the boost for this query
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        return self.set_query_param('boost', float(boost))

    def set_analyzer(self, analyzer):
        """
        Set the analyzer for this query
        @param analyzer:
        @type analyzer: str
        @return:
        @rtype: self
        """
        return self.set_query_param('analyzer', analyzer)

    def set_disable_coord(self, disable=True):
        """
        Enable / disable computation of score factor based on the fraction of all query terms contained in the document
        @param disable: coord is enabled by default
        @type disable: bool
        @return:
        @rtype: self
        """
        return self.set_query_param('disable_coord', bool(disable))
    
    def set_query_param(self, key, value):
        """
        Set a parameter which will go in the body of this query
        @param key: parameter key
        @type key: str
        @param value: parameter value
        @type value: mixed
        @return:
        @rtype: self
        """
        self._query_params[key] = value
        return self

    def to_dict(self):
        """
        @return:
        @rtype: dict
        """
        self.set_param(self._field, self._query_params)
        return super(Common, self).to_dict()



