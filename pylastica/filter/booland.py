__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractMulti

class BoolAnd(AbstractMulti):
    def _get_base_name(self):
        return 'and'
