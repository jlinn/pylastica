__author__ = 'Joe Linn'

from .abstractfacet import AbstractFacet
import pylastica.exception


class GeoDistance(AbstractFacet):
    """
    @see: http://www.elasticsearch.org/guide/reference/api/search/facets/geo-distance-facet/
    """

    def set_ranges(self, ranges):
        """
        Set all ranges for the facet
        @param ranges: [{'to': 50}, {'to': 40, 'from': 20}]
        @type ranges: list of dict
        @return:
        @rtype: self
        """
        return self.set_param('ranges', ranges)

    def add_range(self, range_from=None, range_to=None):
        """
        Add a range to the facet
        @param range_from: optional. Assumed to be boundless if omitted.
        @type range_from: int
        @param range_to: optional. Assumed to be boundless if omitted.
        @type range_to: int
        @return:
        @rtype: self
        """
        if range_from is None and range_to is None:
            raise pylastica.exception.InvalidException("At least one of range_from and range_to must be set.")
        range_dict = {}
        if range_from is not None:
            range_dict['from'] = range_from
        if range_to is not None:
            range_dict['to'] = range_to
        return self.add_param('ranges', range_dict)

    def set_geo_point(self, type_field, lat, lon):
        """
        Set the relative GeoPoint for this facet
        @param type_field: index type and field (pin.location or foo.bar, for example)
        @type type_field: str
        @param lat: latitude
        @type lat: float
        @param lon: longitude
        @type lon: float
        @return:
        @rtype: self
        """
        return self.set_param(type_field, {'lat': lat, 'lon': lon})

    def set_value_field(self, field):
        """
        Set the value field for this facet
        @param field: field name
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param('value_field', field)

    def set_value_script(self, script):
        """
        Set a script for this facet
        @param script:
        @type script: pylastica.script.Script
        @return:
        @rtype: self
        """
        if not isinstance(script, pylastica.script.Script):
            raise TypeError("script must be an instance of Script: %r" % script)
        return self.set_param('value_script', script.script).set_param('params', script.params)

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        self._set_facet_param('geo_distance', self._params)
        return super(GeoDistance, self).to_dict()


