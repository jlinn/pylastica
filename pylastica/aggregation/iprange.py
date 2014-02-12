__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class IpRange(abstract.AbstractAggregation):
    def __init__(self, name, field):
        """
        @param name: the name of this aggregation
        @type name: str
        @param field: the name of the document field on which to perform this aggregation
        @type field: str
        """
        super(IpRange, self).__init__(name)
        self.set_field(field)

    def set_field(self, field):
        """
        Set the field for this aggregation
        @param field: the name of the document field on which to perform this aggregation
        @type field: str
        @return:
        @rtype: IpRange
        """
        return self.set_param("field", field)

    def add_range(self, from_value=None, to_value=None):
        """
        Add an ip range to this aggregation
        @param from_value: A valid ipv4 address. Low end of this range, exclusive (greater than)
        @type from_value: str
        @param to_value: A valid ipv4 address. High end of this range, exclusive (less than)
        @type to_value: str
        @return:
        @rtype: IpRange
        """
        if from_value is None and to_value is None:
            raise ValueError("Either from_value or to_value must be set. Both cannot be None.")
        range = {}
        if from_value is not None:
            range['from'] = from_value
        if to_value is not None:
            range['to'] = to_value
        return self.add_param('ranges', range)

    def add_mask_range(self, mask):
        """
        Add an ip range in the form of a CIDR mask
        @param mask: a valid CIDR mask
        @type mask: str
        @return:
        @rtype: IpRange
        """
        return self.add_param("ranges", {"mask": mask})