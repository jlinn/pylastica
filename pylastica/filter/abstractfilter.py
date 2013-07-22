__author__ = 'Joe Linn'

import abc
import pylastica.param
import pylastica.exception


class AbstractFilter(pylastica.param.Param):
    __metaclass__ = abc.ABCMeta

    def set_cached(self, cached=True):
        """
        Sets the filter cache
        @param cached:
        @type cached: bool
        @return:
        @rtype: self
        """
        return self.set_param('_cache', bool(cached))

    def set_cache_key(self, cache_key):
        """
        Set the filter cache key
        @param cache_key:
        @type cache_key: str
        @return:
        @rtype: self
        """
        self.set_param('_cache_key', str(cache_key))

    def set_name(self, name):
        """
        Set the filter name
        @param name:
        @type name: str
        @return:
        @rtype: self
        """
        return self.set_param('_name', name)


class AbstractGeoDistance(AbstractFilter):
    __metaclass__ = abc.ABCMeta

    LOCATION_TYPE_GEOHASH = 'geohash'
    LOCATION_TYPE_LATLON = 'latlon'

    def __init__(self, key, location):
        """

        @param key:
        @type key: str
        @param location: location as dict or geohash {'lat':40.3, 'lon':45.2}
        @type location: dict or str
        """
        super(AbstractGeoDistance, self).__init__()
        self._location_type = None
        self._key = None
        self._latitude = None
        self._longitude = None
        self._geohash = None
        self.set_key(key)
        self.set_location(location)

    def set_key(self, key):
        """
        Set the key
        @param key:
        @type key: str
        @return:
        @rtype: self
        """
        self._key = str(key)
        return self

    def set_location(self, location):
        """
        Set the location
        @param location:
        @type location: dict or str
        @return:
        @rtype: self
        """
        if isinstance(location, dict):
            if 'lat' in location:
                self.set_latitude(location['lat'])
            else:
                raise pylastica.exception.InvalidException("location['lat'] must be set.")
            if 'lon' in location:
                self.set_longitude(location['lon'])
            else:
                raise pylastica.exception.InvalidException("location['lon'] must be set.")
        elif isinstance(location, str):
            self.set_geohash(location)
        else:
            raise pylastica.exception.InvalidException("location must ba a dict or a string.")
        return self

    def set_latitude(self, lat):
        """

        @param lat:
        @type lat: float
        @return:
        @rtype: self
        """
        self._latitude = float(lat)
        self._location_type = self.LOCATION_TYPE_LATLON
        return self

    def set_longitude(self, lon):
        """

        @param lon:
        @type lon: float
        @return:
        @rtype: self
        """
        self._longitude = float(lon)
        self._location_type = self.LOCATION_TYPE_LATLON
        return self

    def set_geohash(self, geohash):
        """

        @param geohash:
        @type geohash: str
        @return:
        @rtype: self
        """
        self._geohash = geohash
        self._location_type = self.LOCATION_TYPE_GEOHASH
        return self

    def _get_location_data(self):
        """

        @rtype: dict or str
        """
        if self._location_type == self.LOCATION_TYPE_LATLON:
            location = {}
            if self._latitude is not None:
                location['lat'] = self._latitude
            else:
                raise pylastica.exception.InvalidException("Latitude must be set.")
            if self._longitude is not None:
                location['lon'] = self._longitude
            else:
                raise pylastica.exception.InvalidException("Longitude must be set.")
        elif self._location_type == self.LOCATION_TYPE_GEOHASH:
            location = self._geohash
        else:
            raise pylastica.exception.InvalidException("Invalid location type.")
        return location

    def to_dict(self):
        self.set_param(self._key, self._get_location_data())
        return super(AbstractGeoDistance, self).to_dict()


class AbstractMulti(AbstractFilter):
    def __init__(self):
        super(AbstractMulti, self).__init__()
        self._filters = []

    def add_filter(self, filter_object):
        """
        Add a filter
        @param filter_object:
        @type filter_object: AbstractFilter
        @return:
        @rtype: self
        """
        assert isinstance(filter_object, AbstractFilter), "filter must be an instance of an implementation of AbstractFilter: %r" % filter_object
        self._filters.append(filter_object.to_dict())
        return self

    def set_filters(self, filters):
        """
        Set filters
        @param filters:
        @type filters: list of AbstractFilter
        @return:
        @rtype: self
        """
        self._filters = []
        for filter_object in filters:
            self.add_filter(filter_object)
        return self

    def to_dict(self):
        data = super(AbstractMulti, self).to_dict()
        name = self._get_base_name()
        filter_data = data[name]
        if filter_data is None:
            filter_data = self._filters
        else:
            filter_data['filters'] = self._filters
        data[name] = filter_data
        return data
