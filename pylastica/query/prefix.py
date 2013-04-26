__author__ = 'Joe Linn'

import pylastica

class Prefix(pylastica.query.AbstractQuery):
    def __init__(self, prefix=None):
        """

        @param prefix:
        @type prefix: dict of str
        """
        self.set_raw_prefix(prefix)

    def set_raw_prefix(self, prefix):
        """
        Set values for the prefix
        @param prefix:
        @type prefix: dict of str
        @return:
        @rtype: self
        """
        if prefix is None:
            prefix = {}
        self.params = prefix
        return self

    def set_prefix(self, key, value, boost=1.0):
        """
        Set the prefix for this query
        @param key: key to query
        @type key: str
        @param value: value(s) for the query
        @type value: str or list of str
        @param boost: optional, defaults to 1.0
        @type boost: float
        @return:
        @rtype: self
        """
        return self.set_raw_prefix({key: {'value': value, 'boost': boost}})
