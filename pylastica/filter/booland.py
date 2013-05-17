__author__ = 'Joe Linn'

import pylastica.filter.abstractfilter

class BoolAnd(pylastica.filter.abstractfilter.AbstractMulti):
    def _get_base_name(self):
        return 'and'
