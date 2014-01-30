__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class Nested(abstract.AbstractAggregation):
    def set_path(self, path):
        """
        Set the nested path for this aggregation
        @param path:
        @type path: str
        @return:
        @rtype: Nested
        """
        return self.set_param("path", path)