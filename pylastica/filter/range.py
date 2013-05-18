__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter

class Range(AbstractFilter):
    def __init__(self, field_name=None, args=None):
        """

        @param field_name: field name
        @type field_name: str
        @param args: field arguments
        @type args: dict
        @see: http://www.elasticsearch.org/guide/reference/query-dsl/range-filter/
        """
        super(Range, self).__init__()
        self._fields = {}
        if field_name is not None:
            self.add_field(field_name, args)

    def add_field(self, field_name, args):
        """
        Add a field with arguments to the range filter
        @param field_name: field name
        @type field_name: str
        @param args: field arguments
        @type args: dict
        @return:
        @rtype: self
        """
        self._fields[field_name] = args
        return self

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        self.params = self._fields
        return super(Range, self).to_dict()

