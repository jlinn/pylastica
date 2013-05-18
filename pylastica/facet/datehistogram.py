__author__ = 'Joe Linn'

from .histogram import Histogram

class DateHistogram(Histogram):
    """
    @see: http://www.elasticsearch.org/guide/reference/api/search/facets/date-histogram-facet/
    """

    def set_timezone(self, offset):
        """
        Set the time_zone parameter
        @param offset:
        @type offset: str
        @return:
        @rtype: self
        """
        return self.set_param('time_zone', offset)

    def set_factor(self, factor):
        """
        Set the conversion factor for time values
        @param factor: 1000 to convert stored seconds data to milliseconds, for example
        @type factor: int
        @return:
        @rtype: self
        """
        return self.set_param('factor', factor)

    def set_pre_offset(self, offset):
        """
        Set pre rounding offset
        @param offset: date / time offset (1h, 1d, 1s, etc.)
        @type offset: str
        @return:
        @rtype: self
        """
        return self.set_param('pre_offset', offset)

    def set_post_offset(self, offset):
        """
        Set post rounding offset
        @param offset: date / time offset (1h, 1d, 1s, etc.)
        @type offset: str
        @return:
        @rtype: self
        """
        return self.set_param('post_offset', offset)

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        self._set_facet_param('date_histogram', self._params)
        return self._facet


