__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class Range(abstract.SimpleAggregation):
    def add_range(self, from_value=None, to_value=None):
        """
        Add a range for this aggregation
        @param from_value: low end of this range, exclusive (greater than)
        @type from_value: int or float
        @param to_value: high end of this range, exclusive (less than)
        @type to_value: int or float
        @return:
        @rtype: Range
        """
        if from_value is None and to_value is None:
            raise ValueError("Either from_value or to_value must be set. Both cannot be None.")
        range = {}
        if from_value is not None:
            range['from'] = from_value
        if to_value is not None:
            range['to'] = to_value
        return self.add_param('ranges', range)

    def set_keyed_response(self, keyed=True):
        """
        If set to True, a unique string key will be associated with each bucket and ranges will be returned as a
        dictionary rather than a list.
        @param keyed:
        @type keyed: bool
        @return:
        @rtype: Range
        """
        return self.set_param('keyed', keyed)