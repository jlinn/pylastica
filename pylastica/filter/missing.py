__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter

class Missing(AbstractFilter):
    def __init__(self, field=''):
        """

        @param field: field name
        @type field: str
        """
        super(Missing, self).__init__()
        if len(field):
            self.set_field(field)

    def set_field(self, field):
        """
        Set the field
        @param field: document field
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param('field', str(field))
