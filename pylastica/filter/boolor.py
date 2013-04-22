__author__ = 'Joe Linn'

import pylastica.filter

class BoolOr(pylastica.filter.AbstractMulti):
    def _get_base_name(self):
        """

        @return:
        @rtype: str
        """
        return 'or'
