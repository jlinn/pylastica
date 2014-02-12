__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class ValueCount(abstract.AbstractAggregation):
    def __init__(self, name, field):
        """
        @param name: the name of this aggregation
        @type name: str
        @param field: the name of the document field on which to perform this aggregation
        @type field: str
        """
        super(ValueCount, self).__init__(name)
        self.set_field(field)

    def set_field(self, field):
        """
        Set the field for this aggregation
        @param field: the name of the document field on which to perform this aggregation
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param("field", field)