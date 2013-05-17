__author__ = 'Joe Linn'

import pylastica.filter.abstractfilter
import pylastica.exception

class GeoPolygon(pylastica.filter.abstractfilter.AbstractFilter):
    def __init__(self, key, points):
        """
        @param key:
        @type key: str
        @param points: points making up the polygon [{'lat': float, 'lon': float}]
        @type points: list of dict
        """
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


