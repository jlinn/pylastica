__author__ = 'Joe Linn'

import pylastica.filter

class BoolAnd(pylastica.filter.AbstractMulti):
    def _get_base_name(self):
        return 'and'
