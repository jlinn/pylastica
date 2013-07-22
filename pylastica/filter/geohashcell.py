__author__ = 'Joe Linn'

from .abstractfilter import AbstractGeoDistance


class GeohashCell(AbstractGeoDistance):
    def __init__(self, key, location, precision=-1, neighbors=False):
        """
        @param key: The field on which to filter
        @type key: str
        @param location: location as dict or geohash {'lat':40.3, 'lon':45.2}
        @type location: str or dict
        @param precision: Optional. Integer length of geohash prefix or distance (3, or "50m")
        @type precision: str or int
        @param neighbors: If true, filters cells next to the given cell. Defaults to False.
        @type neighbors: bool
        """
        super(GeohashCell, self).__init__(key, location)
        self.set_precision(precision)
        self.set_neighbors(neighbors)

    def set_precision(self, precision):
        """
        Set the precision for this filter
        @param precision: Integer length of geohash prefix or distance (3, or "50m")
        @type precision: str or int
        @return:
        @rtype: self
        """
        return self.set_param('precision', precision)

    def set_neighbors(self, neighbors):
        """
        Set the neighbors option for this filter
        @param neighbors: If true, filters cells next to the given cell.
        @type neighbors: bool
        @return:
        @rtype: self
        """
        return self.set_param('neighbors', bool(neighbors))