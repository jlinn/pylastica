__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractMulti

class BoolOr(AbstractMulti):
    def _get_base_name(self):
        """

        @return:
        @rtype: str
        """
        return 'or'
