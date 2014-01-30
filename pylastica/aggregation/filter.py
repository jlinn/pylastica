__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract
import pylastica.filter.abstractfilter as abstractfilter


class Filter(abstract.AbstractAggregation):
    def set_filter(self, filter):
        """
        Set the filter for this aggregation
        @param filter: the filter to use for this aggregation
        @type filter: pylastica.filter.abstractfilter.AbstractFilter
        @return:
        @rtype: Filter
        """
        if not isinstance(filter, abstractfilter.AbstractFilter):
            raise TypeError("filter must be an instance of an implementation of AbstractFilter: %r" % filter)
        return self.set_param("filter", filter.to_dict())

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        return {
            "filter": self.get_param("filter"),
            "aggs": self._aggs
        }