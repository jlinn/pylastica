__author__ = 'Joe Linn'

from .abstractfilter import AbstractGeoDistance
import pylastica.exception


class GeoDistanceRange(AbstractGeoDistance):
    RANGE_FROM = 'from'
    RANGE_TO = 'to'
    RANGE_LT = 'lt'
    RANGE_LTE = 'lte'
    RANGE_GT = 'gt'
    RANGE_GTE = 'gte'

    RANGE_INCLUDE_LOWER = 'include_lower'
    RANGE_INCLUDE_UPPER = 'include_upper'

    def __init__(self, key, location, lower=None, upper=None, include_lower=True, include_upper=True):
        """
        @param key:
        @type key: str
        @param location: location as dict or geohash {'lat':40.3, 'lon':45.2}
        @type location: dict or str
        @param lower: lower bound of range
        @type lower: float or int or str
        @param upper: upper bound of range
        @type upper: float or int or str
        @param include_lower:
        @type include_lower: bool
        @param include_upper:
        @type include_upper: bool
        """
        super(GeoDistanceRange, self).__init__(key, location)
        self._ranges = {}
        if lower is not None or upper is not None:
            self.set_range(lower, upper, include_lower, include_upper)


    def set_range(self, lower=None, upper=None, include_lower=False, include_upper=False):
        """
        @param lower: lower bound of range
        @type lower: float or int or str
        @param upper: upper bound of range
        @type upper: float or int or str
        @param include_lower:
        @type include_lower: bool
        @param include_upper:
        @type include_upper: bool
        @return:
        @rtype: self
        """
        if lower is None and upper is None:
            raise pylastica.exception.InvalidException("Either lower or upper must be given a value.")
        value = {}
        if lower is not None:
            value[self.RANGE_FROM] = lower
            value[self.RANGE_INCLUDE_LOWER] = bool(include_lower)
        if upper is not None:
            value[self.RANGE_TO] = upper
            value[self.RANGE_INCLUDE_UPPER] = bool(include_upper)
        self._ranges = value
        return self

    def to_dict(self):
        for key, value in self._ranges.iteritems():
            self.set_param(key, value)
        return super(GeoDistanceRange, self).to_dict()


