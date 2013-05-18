__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter
import pylastica.exception

class GeoBoundingBox(AbstractFilter):
    def __init__(self, key, coordinates):
        """
        @param key:
        @type key: str
        @param coordinates: list with top left coordinates as first index, and bottom right coordinates as second index
        @type coordinates: list
        """
        super(GeoBoundingBox, self).__init__()
        self.add_coordinates(key, coordinates)

    def add_coordinates(self, key, coordinates):
        """
        Add coordinates
        @param key:
        @type key: str
        @param coordinates: list with top left coordinates as first index, and bottom right coordinates as second index
        @type coordinates: list
        @return:
        @rtype: self
        """
        if len(coordinates) != 2:
            raise pylastica.exception.InvalidException("Expected coordinates to be a list with two elements.")
        self.set_param(key, {
            'top_left': coordinates[0],
            'bottom_right': coordinates[1]
        })
        return self
