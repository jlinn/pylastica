__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter

class BoolNot(AbstractFilter):
    def __init__(self, filter_object):
        super(BoolNot, self).__init__()
        self.set_filter(filter_object)

    def set_filter(self, filter_object):
        """
        Set filter
        @param filter_object:
        @type filter_object: pylastica.filter.AbstractFilter
        @return:
        @rtype: self
        """
        assert isinstance(filter_object, AbstractFilter), "filter_object must be in instance of an implementation of AbstractFilter: %r" % filter_object
        return self.set_param('filter',filter_object.to_dict())

    def _get_base_name(self):
        """

        @return:
        @rtype: str
        """
        return 'not'
