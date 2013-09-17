__author__ = 'Joe Linn'

from .abstract import AbstractQuery
from pylastica.filter.abstractfilter import AbstractFilter


class FunctionScore(AbstractQuery):
    """
    @see http://www.elasticsearch.org/guide/reference/query-dsl/function-score-query/
    """

    BOOST_MODE_MULTIPLY = 'multiply'
    BOOST_MODE_REPLACE = 'replace'
    BOOST_MODE_SUM = 'sum'
    BOOST_MODE_AVERAGE = 'avg'
    BOOST_MODE_MAX = 'max'
    BOOST_MODE_MIN = 'min'

    SCORE_MODE_MULTIPLY = 'multiply'
    SCORE_MODE_SUM = 'sum'
    SCORE_MODE_AVERAGE = 'avg'
    SCORE_MODE_FIRST = 'first'
    SCORE_MODE_MAX = 'max'
    SCORE_MODE_MIN = 'min'

    DECAY_GAUSS = 'gauss'
    DECAY_EXPONENTIAL = 'exp'
    DECAY_LINEAR = 'linear'

    def __init__(self):
        super(FunctionScore, self).__init__()
        self._functions = []

    def set_query(self, query):
        """
        Set the query for this function_score query
        @param query: a Query object
        @type query: pylastica.query.AbstractQuery
        @return:
        @rtype: self
        """
        if not isinstance(query, AbstractQuery):
            raise TypeError("query must be and instance of a descendant of AbstractQuery: %r" % query)
        self.set_param('query', query.to_dict())

    def set_filter(self, filter):
        """
        Set the filter for this function_score query
        @param filter:
        @type filter: AbstractFilter
        @return:
        @rtype: self
        """
        return self.set_param('filter', filter.to_dict())

    def add_function(self, function_type, function_params, filter=None, boost=None):
        """
        Add a function to the function_score query
        @param function_type: valid values are gauss, exp, linear, script_score
        @type function_type: str
        @param function_params: the body of the function. See documentation for proper syntax.
        @type function_params: dict
        @param filter: an optional filter to apply to the function
        @type filter: pylastica.filter.AbstractFilter
        @param boost: optional boost value associated with this function
        @type boost: float
        @return:
        @rtype: self
        """
        function = {
            function_type: function_params
        }
        if filter is not None:
            if not isinstance(filter, AbstractFilter):
                raise TypeError("filter must be an instance of a descendant of AbstractFilter: %r" % filter)
            function['filter'] = filter.to_dict()
        if boost is not None:
            function['boost'] = float(boost)
        self._functions.append(function)
        return self

    def add_script_score_function(self, script, filter=None, boost=None):
        """
        Add a script_score function to the query
        @param script: a Script object
        @type script: pylastica.Script
        @param filter: a filter object
        @type filter: AbstractFilter
        @param boost: optional boost value associated with this function
        @type boost: float
        @return:
        @rtype: self
        """
        return self.add_function('script_score', script.to_dict(), filter, boost)

    def add_decay_function(self, function, field, origin, scale, offset=None, decay=None, scale_weight=None,
                           filter=None, boost=None):
        """
        Add a decay function to the query
        @param function: the decay function type. See DECAY_* properties for valid options.
        @type function: str
        @param field: the document field on which to perform the decay function
        @type field: str
        @param origin: the origin value for this decay function
        @type origin: str
        @param scale: a scale to define the rate of decay for this function
        @type scale: str
        @param offset: optional. If defined, this function will only be computed for documents with a distance greater than this value.
        @type offset: str
        @param decay: optionally defines how documents are scored at the distance given in the scale parameter
        @type decay: float
        @param scale_weight: an optional factor by which to multiply the score at the value provided by the scale parameter
        @type scale_weight: float
        @param filter: a filter associated with this function
        @type filter: AbstractFilter
        @param boost: an optional boost value associated with this function
        @type boost: float
        @return:
        @rtype: self
        """
        valid_decay = [
            self.DECAY_GAUSS,
            self.DECAY_EXPONENTIAL,
            self.DECAY_LINEAR
        ]
        if function not in valid_decay:
            raise ValueError("%s is not a supported decay function." % function)
        function_params = {
            field: {
                'origin': origin,
                'scale': scale
            }
        }
        if offset is not None:
            function_params[field]['offset'] = offset
        if decay is not None:
            function_params[field]['decay'] = float(decay)
        if scale_weight is not None:
            function_params[field]['scale_weight'] = float(scale_weight)
        return self.add_function(function, function_params, filter, boost)

    def set_boost(self, boost=1.0):
        """
        Set the boost for the query
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        return self.set_param('boost', float(boost))

    def set_max_boost(self, max_boost):
        """
        Restrict the combined boost of the function_score query and its child query
        @param max_boost:
        @type max_boost: float
        @return:
        @rtype: self
        """
        return self.set_param('max_boost', float(max_boost))

    def set_boost_mode(self, mode):
        """
        The boost mode determines how the score of this query is combined with that of the child query
        @param mode: see BOOST_MODE_* properties for valid options. Default is multiply.
        @type mode: str
        @return:
        @rtype: self
        """
        valid_boost_modes = [
            self.BOOST_MODE_MULTIPLY,
            self.BOOST_MODE_REPLACE,
            self.BOOST_MODE_SUM,
            self.BOOST_MODE_AVERAGE,
            self.BOOST_MODE_MAX,
            self.BOOST_MODE_MIN
        ]
        if mode not in valid_boost_modes:
            raise ValueError("%s is not a valid boost mode." % mode)
        return self.set_param('boost_mode', mode)

    def set_random_score(self, seed=None):
        """
        If set, this query will return results in random order.
        @param seed: Set a seed value to return results in the same random order for consistent pagination.
        @type seed: int
        @return:
        @rtype: self
        """
        seed_param = {}
        if seed is not None:
            seed_param['seed'] = int(seed)
        return self.set_param('random_score', seed_param)

    def set_score_mode(self, mode):
        """
        Set score method
        @param mode: see SCORE_MODE_* properties for options. Default is multiply.
        @type mode: str
        @return:
        @rtype: self
        """
        valid_score_modes = [
            self.SCORE_MODE_MULTIPLY,
            self.SCORE_MODE_SUM,
            self.SCORE_MODE_AVERAGE,
            self.SCORE_MODE_FIRST,
            self.SCORE_MODE_MAX,
            self.SCORE_MODE_MIN
        ]
        if mode not in valid_score_modes:
            raise ValueError("%s is not a valid score mode." % mode)
        return self.set_param('score_mode', mode)

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        if len(self._functions):
            self.set_param('functions', self._functions)
        return super(FunctionScore, self).to_dict()
