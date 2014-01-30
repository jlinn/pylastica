__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class DateRange(abstract.AbstractAggregation):
    def set_field(self, field):
        """
        Set the field for this aggregation
        @param field: the name of the document field on which to perform this aggregation
        @type field: str
        @return:
        @rtype: DateRange
        """
        return self.set_param("field", field)

    def add_range(self, from_value=None, to_value=None):
        """
        Add a date range for this aggregation.
        See documentation for valid date formats.
        @see http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-aggregations-bucket-daterange-aggregation.html
        @param from_value: low end of this range, exclusive (greater than)
        @type from_value: str or int
        @param to_value: high end of this range, exclusive (less than)
        @type to_value: str or int
        @return:
        @rtype: DateRange
        """
        if from_value is None and to_value is None:
            raise ValueError("Either from_value or to_value must be set. Both cannot be None.")
        range = {}
        if from_value is not None:
            range['from'] = from_value
        if to_value is not None:
            range['to'] = to_value
        return self.add_param('ranges', range)

    def set_format(self, format):
        """
        Set the format of the date values to be returned
        @param format: see documentation for formatting options
        @type format: str
        @return:
        @rtype: DateRange
        """
        return self.set_param("format", format)