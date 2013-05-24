__author__ = 'Joe Linn'

from .abstract import *


class ConstantScore(AbstractQuery):
    def __init__(self, filter=None):
        """

        @param filter:
        @type filter: dict or pylastica.filter.AbstractFilter
        """
        super(ConstantScore, self).__init__()
        if filter is not None:
            self.set_filter(filter)

    def set_filter(self, filter):
        """
        Set the filter for this query
        @param filter:
        @type filter: dict or pylastica.filter.AbstractFilter
        @return:
        @rtype: self
        """
        if isinstance(filter, pylastica.filter.AbstractFilter):
            filter = filter.to_dict()
        return self.set_param('filter', filter)

    def set_boost(self, boost):
        """
        Set boost
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        return self.set_param('boost', boost)
