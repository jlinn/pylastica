__author__ = 'Joe Linn'

from .abstract import AbstractQuery


class Field(AbstractQuery):
    def __init__(self, field='', query_string=''):
        """

        @param field: optional field name
        @type field: str
        @param query_string: optional query string
        @type query_string: str
        """
        super(Field, self).__init__()
        self.set_field(field).set_query_string(query_string)

    def set_field(self, field):
        """
        Set the field
        @param field:
        @type field: str
        @return:
        @rtype: self
        """
        self._field = str(field)
        return self

    def set_query_string(self, query_string):
        """
        Set a new query string
        @param query_string:
        @type query_string: str
        @return:
        @rtype: self
        """
        assert isinstance(query_string, str), "query_string must be a str: %r" % query_string
        self._query_string = query_string
        return self

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        self.set_param(self._field, {'query': self._query_string})
        return super(Field, self).to_dict()


