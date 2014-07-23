__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class TopHits(abstract.AbstractAggregation):
    def set_from(self, from_offset):
        """
        Set the offset of the first result to be fetched
        @param from_offset: offset of the first result
        @type from_offset: int
        @return:
        @rtype: self
        """
        return self.set_param("from", from_offset)

    def set_size(self, size):
        """
        Set the maximum number of hits to return per bucket
        @param size: hits to return per bucket
        @type size: int
        @return:
        @rtype: self
        """
        return self.set_param("size", size)

    def set_sort(self, sort):
        """
        Set the sort order for matching hits
        @param sort: sort order
        @type sort: str
        @return:
        @rtype: self
        """
        return self.set_param("sort", sort)