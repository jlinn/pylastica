
__author__ = 'Joe Linn'

import abc
from pylastica.param import Param


class AbstractAggregation(Param):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        super(AbstractAggregation, self).__init__()
        self._name = None
        self.name = name

    @property
    def name(self):
        """
        Get the name of this facet
        @return:
        @rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name of this facet.
        @param name:
        @type name: str
        """
        if not isinstance(name, str) or name == '':
            raise TypeError("name must be a string: %r" % name)
        self._name = name

    def add_aggregation(self, aggregation):
        """
        Add a sub-aggregation
        @param aggregation: a sub-aggregation
        @type aggregation: AbstractAggregation
        @return:
        @rtype: self
        """
        if not isinstance(aggregation, AbstractAggregation):
            raise TypeError("aggregation must be an implementation of AbstractAggregation: %r" % aggregation)
        if 'aggs' not in self._params:
            self._params['aggs'] = {}
        self._params['aggs'][aggregation.name] = aggregation.to_dict()
        return self