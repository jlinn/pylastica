__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class GeoDistance(abstract.AbstractAggregation):
    def __init__(self, name, field, origin):
        """
        @param name: the name of this aggregation
        @type name: str
        @param field: the field on which to perform this aggregation
        @type field: str
        @param origin: the point from which distances will be calculated
        @type origin: dict or str or list
        """
        super(GeoDistance, self).__init__(name)
        self.set_field(field).set_origin(origin)

    def set_field(self, field):
        """
        Set the field for this aggregation
        @param field: the name of the document field on which to perform this aggregation
        @type field: str
        @return:
        @rtype: GeoDistance
        """
        return self.set_param("field", field)

    def set_origin(self, origin):
        """
        Set the origin point from which distances will be calculated
        @param origin: valid formats are { "lat" : 52.3760, "lon" : 4.894 }, "52.3760, 4.894", and [4.894, 52.3760]
        @type origin: dict or str or list
        @return:
        @rtype: GeoDistance
        """
        return self.set_param("origin", origin)

    def add_range(self, from_value=None, to_value=None):
        """
        Add a distance range to this aggregation
        @param from_value: A distance
        @type from_value: int
        @param to_value: A distnace
        @type to_value: int
        @return:
        @rtype: GeoDistance
        """
        if from_value is None and to_value is None:
            raise ValueError("Either from_value or to_value must be set. Both cannot be None.")
        range = {}
        if from_value is not None:
            range['from'] = from_value
        if to_value is not None:
            range['to'] = to_value
        return self.add_param('ranges', range)

    def set_unit(self, unit):
        """
        Set the unit of distance measure for this aggregation
        @param unit: defaults to km
        @type unit: str
        @return:
        @rtype: GeoDistance
        """
        return self.set_param("unit", unit)

    def set_distance_type(self, distance_type):
        """
        Set the method by which distances will be calculated
        @param distance_type: valid options are sloppy_arc (default), arc, and plane
        @type distance_type: str
        @return:
        @rtype: GeoDistance
        """
        return self.set_param("distance_type", distance_type)