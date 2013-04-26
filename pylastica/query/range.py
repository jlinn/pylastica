__author__ = 'Joe Linn'

import pylastica

class Range(pylastica.query.AbstractQuery):
    def __init__(self, field_name=None, args=None):
        if field_name:
            self.add_field(field_name, args)

    def add_field(self, field_name, args=None):
        """
        Add a range field to the query
        @param field_name:
        @type field_name: str
        @param args:
        @type args: dict
        @return:
        @rtype: self
        """
        if args is None:
            args = {}
        return self.set_param(field_name, args)
