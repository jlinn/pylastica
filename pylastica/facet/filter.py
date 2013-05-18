__author__ = 'Joe Linn'

from .abstractfacet import AbstractFacet
import pylastica.filter.abstractfilter


class Filter(AbstractFacet):
    def set_filter(self, filter_object):
        """
        Set the filter for the facet
        @param filter_object:
        @type filter_object: pylastica.filter.abstractfilter.AbstractFilter
        @return:
        @rtype: self
        """
        if not isinstance(filter_object, pylastica.filter.abstractfilter.AbstractFilter):
            raise TypeError("filter_object must be an instance of an implementation of AbstractFilter: %r" % filter_object)
        return self._set_facet_param('filter', filter_object.to_dict())

