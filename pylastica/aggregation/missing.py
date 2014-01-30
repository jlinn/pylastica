__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class Missing(abstract.AbstractAggregation):
    def set_field(self, field):
        """
        Set the field for this aggregation
        @param field: the name of the document field on which to perform this aggregation
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param("field", field)