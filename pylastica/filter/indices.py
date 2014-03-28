__author__ = 'Joe Linn'

import pylastica.filter.abstractfilter as abstractfilter


class Indices(abstractfilter.AbstractFilter):
    def __init__(self, filter, indices):
        """

        @param filter:
        @type filter: abstractfilter.AbstractFilter
        @param indices:
        @type indices: list of str
        """
        super(Indices, self).__init__()
        self.set_indices(indices).set_filter(filter)

    def set_indices(self, indices):
        """
        Set the names of the indices on which this filter should be applied
        @param indices: a list of index names
        @type indices: list of str
        @return:
        @rtype: self
        """
        return self.set_param("indices", indices)

    def set_filter(self, filter):
        """
        Set the filter to be applied to the docs in the specified indices
        @param filter:
        @type filter: abstractfilter.AbstractFilter
        @return:
        @rtype: self
        """
        if not isinstance(filter, abstractfilter.AbstractFilter):
            raise TypeError("filter must be an implementation of AbstractFilter: %r" % filter)
        return self.set_param("filter", filter.to_dict())

    def set_no_match_filter(self, filter):
        """
        Set the filter to be applied to docs in indices which do not match those specified in the "indices" parameter
        @param filter:
        @type filter: abstractfilter.AbstractFilter
        @return:
        @rtype: self
        """
        if not isinstance(filter, abstractfilter.AbstractFilter):
            raise TypeError("filter must be an implementation of AbstractFilter: %r" % filter)
        return self.set_param("no_match_filter", filter.to_dict())