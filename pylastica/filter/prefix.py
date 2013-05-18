__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter

class Prefix(AbstractFilter):
    def __init__(self, field='', prefix=''):
        """
        @param field: field name
        @type field: str
        @param prefix: prefix string
        @type prefix: str
        """
        super(Prefix, self).__init__()
        self.set_field(field)
        self.set_prefix(prefix)

    def set_field(self, field):
        """
        Set the name of the prefix field
        @param field: field name
        @type field: str
        @return:
        @rtype: self
        """
        self._field = field
        return self

    def set_prefix(self, prefix):
        """
        Set the prefix string
        @param prefix:
        @type prefix: str
        @return:
        @rtype: self
        """
        self._prefix = prefix
        return self

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        self.set_param(self._field, self._prefix)
        return super(Prefix, self).to_dict()


