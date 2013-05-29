__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter
import pylastica.exception

class GeoPolygon(AbstractFilter):
    def __init__(self, key, points):
        """
        @param key:
        @type key: str
        @param points: points making up the polygon [{'lat': float, 'lon': float}]
        @type points: list of list or list of dict
        """
        super(GeoPolygon, self).__init__()
        self._key = key
        self._points = points

    def to_dict(self):
        """
        @rtype : dict
        """
        return {
            'geo_polygon':{
                self._key:{
                    'points': self._points
                }
            }
        }


