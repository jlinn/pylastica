__author__ = 'Joe Linn'

import pylastica

class Wildcard(pylastica.query.AbstractQuery):
    def __init__(self, key='', value=None, boost=1.0):
        """

        @param key: wildcard key
        @type key: str
        @param value: wildcard value
        @type value: str
        @param boost:
        @type boost: float
        """
        if key != '':
            self.set_value(key, value, boost)

    def set_value(self, key, value, boost=1.0):
        """
        Set the query expression for a key with a boost value
        @param key:
        @type key: str
        @param value:
        @type value: str
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        return self.set_param(key, {'value': value, 'boost': boost})
