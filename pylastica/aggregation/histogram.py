__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class Histogram(abstract.SimpleAggregation):
    def __init__(self, name, field, interval):
        """
        @param name: the name of this aggregation
        @type name: str
        @param field: the field on which to perform this aggregation
        @type field: str
        @param interval: the interval by which documents will be bucketed
        @type interval: int
        """
        super(Histogram, self).__init__(name)
        self.set_field(field).set_interval(interval)

    def set_interval(self, interval):
        """
        Set the interval by which documents will be bucketed
        @param interval:
        @type interval: int
        @return:
        @rtype: Histogram
        """
        return self.set_param("interval", interval)

    def set_order(self, order, direction):
        """
        Set the bucket sort order
        @param order: _count, _term, or the name of a sub-aggregation or sub-aggregation response field
        @type order: str
        @param direction: asc or desc
        @type direction: str
        @return:
        @rtype: Histogram
        """
        return self.set_param('order', {order: direction})

    def set_minimum_document_count(self, count):
        """
        Set the minimum number of documents which must fall into a bucket in order for the bucket to be returned
        @param count: set to 0 to include empty buckets
        @type count: int
        @return:
        @rtype: Histogram
        """
        return self.set_param('min_doc_count', count)