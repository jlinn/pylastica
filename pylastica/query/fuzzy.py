__author__ = 'Joe Linn'

from .abstract import AbstractQuery
import pylastica.exception

class Fuzzy(AbstractQuery):
    def __init__(self, field_name=None, value=None):
        """
        Set either both parameters or neither.
        @param field_name: field name
        @type field_name: str
        @param value: search string
        @type value: str
        """
        super(Fuzzy, self).__init__()
        if field_name and value:
            self.set_field(field_name, value)

    def set_field(self, field_name, value):
        """

        @param field_name:
        @type field_name: str
        @param value:
        @type value: str
        @return:
        @rtype: self
        """
        if not isinstance(value, str) or not isinstance(field_name, str):
            raise pylastica.exception.InvalidException("field_name and value parameters must be str.")
        return self.set_param(field_name, {'value': value})

    def set_field_option(self, param, value):
        """
        Set optional parameters
        @param param: option name
        @type param: str
        @param value:
        @type value:
        @return:
        @rtype:
        """
        params = self.params
        if len(params) < 1:
            raise pylastica.exception.InvalidException("No field has been set.")
        params[params.keys()[0]][param] = value
        return self.set_param(params.keys()[0], params[params.keys()[0]])
