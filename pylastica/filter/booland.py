__author__ = 'Joe Linn'

from .abstractfilter import AbstractMulti


class BoolAnd(AbstractMulti):
    """
    @see: @link http://www.elasticsearch.org/guide/reference/query-dsl/and-filter.html
    """
    def _get_base_name(self):
        return 'and'
