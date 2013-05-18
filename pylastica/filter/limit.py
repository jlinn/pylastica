__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter

class Limit(AbstractFilter):
    def __init__(self, limit):
        """
        @param limit: limit
        @type limit: int
        """
        super(Limit, self).__init__()
        self.set_limit(limit)

    def set_limit(self, limit):
        """
        Set the limit
        @param limit:
        @type limit: int
        @return:
        @rtype: self
        """
        return self.set_param('value', int(limit))
