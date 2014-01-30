__author__ = 'Joe Linn'

import pylastica.aggregation.histogram as histogram


class DateHistogram(histogram.Histogram):
    def __init__(self, name, field, interval):
        """
        @param name: the name of this aggregation
        @type name: str
        @param field: the field on which to perform this aggregation
        @type field: str
        @param interval: the interval by which documents will be bucketed
        @type interval: str
        """
        super(DateHistogram, self).__init__(name, field, interval)

    def set_interval(self, interval):
        """
        Set the interval by which documents will be bucketed
        @param interval: "1.5h", for example
        @type interval: str
        @return:
        @rtype: DateHistogram
        """
        return self.set_param("interval", interval)

    def set_pre_zone(self, pre_zone):
        """
        Set pre-rounding based on interval
        @param pre_zone:
        @type pre_zone: str
        @return:
        @rtype: DateHistogram
        """
        return self.set_param("pre_zone", pre_zone)

    def set_post_zone(self, post_zone):
        """
        Set post-rounding based on interval
        @param post_zone:
        @type post_zone: str
        @return:
        @rtype: DateHistogram
        """
        return self.set_param("post_zone", post_zone)

    def set_pre_zone_adjust_large_interval(self, adjust):
        """
        Set pre-zone adjustment for larger time intervals (day and above)
        @param adjust:
        @type adjust: str
        @return:
        @rtype: DateHistogram
        """
        return self.set_param("pre_zone_adjust_large_interval", adjust)

    def set_factor(self, factor):
        """
        Adjust for granularity of date data
        @param factor: set to 1000 if date is stored in seconds rather than milliseconds
        @type factor: int
        @return:
        @rtype: DateHistogram
        """
        return self.set_param("factor", factor)

    def set_pre_offset(self, offset):
        """
        Set the offset for pre-rounding
        @param offset: "1d", for example
        @type offset: str
        @return:
        @rtype: DateHistogram
        """
        return self.set_param("pre_offset", offset)

    def set_post_offset(self, offset):
        """
        Set the offset for post-rounding
        @param offset: "1d", for example
        @type offset: str
        @return:
        @rtype: DateHistogram
        """
        return self.set_param("post_offset", offset)

    def set_format(self, format):
        """
        Set the format for returned bucket key_as_string values
        @param format: see http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-aggregations-bucket-daterange-aggregation.html#date-format-pattern
        @type format: str
        @return:
        @rtype: DateHistogram
        """
        return self.set_param("format", format)