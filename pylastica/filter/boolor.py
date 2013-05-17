__author__ = 'Joe Linn'

import pylastica.filter.abstractfilter

class BoolOr(pylastica.filter.abstractfilter.AbstractMulti):
    def _get_base_name(self):
        """

        @return:
        @rtype: str
        """
        return 'or'
