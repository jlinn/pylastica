__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractGeoDistance

class GeoDistance(AbstractGeoDistance):
    DISTANCE_TYPE_ARC = 'arc'
    DISTANCE_TYPE_PLANE = 'plane'

    OPTIMIZE_BBOX_MEMORY = 'memory'
    OPTIMIZE_BBOX_INDEXED = 'indexed'
    OPTIMIZED_BBOX_NONE = 'none'

    def __init__(self, key, location, distance):
        """
        @param key:
        @type key: str
        @param location: location as dict or geohash {'lat':40.3, 'lon':45.2}
        @type location: dict or str
        @param distance:
        @type distance: str
        """
        super(GeoDistance, self).__init__(key, location)
        self.set_distance(distance)


    def set_distance(self, distance):
        """
        @param distance:
        @type distance: str
        @return:
        @rtype: self
        """
        return self.set_param('distance', distance)

    def set_distance_type(self, distance_type):
        """
        See DISTANCE_TYPE_* class properties
        @param distance_type:
        @type distance_type: str
        @return:
        @rtype: self
        """
        return self.set_param('distance_type', distance_type)

    def set_optimize_bbox(self, optimize):
        """
        See OPTIMIZE_BBOX_* constants
        @param optimize:
        @type optimize: str
        @return:
        @rtype: self
        """
        return self.set_param('optimize_box', optimize)
