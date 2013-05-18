__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter

class Exists(AbstractFilter):
    """
    @see http://www.elasticsearch.org/guide/reference/query-dsl/exists-filter.html
    """
    def __init__(self, field):
        """

        @param field:
        @type field: str
        """
        super(Exists, self).__init__()
        self.set_field(field)

    def set_field(self, field):
        """
        Set field
        @param field:
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param('field', field)
