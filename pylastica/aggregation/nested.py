__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class Nested(abstract.AbstractAggregation):
    def __init__(self, name, path):
        """
        @param name: the name of this aggregation
        @type name: str
        @param path: the nested path for this aggregation
        @type path: str
        """
        super(Nested, self).__init__(name)
        self.set_path(path)

    def set_path(self, path):
        """
        Set the nested path for this aggregation
        @param path:
        @type path: str
        @return:
        @rtype: Nested
        """
        return self.set_param("path", path)