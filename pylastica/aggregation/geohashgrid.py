__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class GeohashGrid(abstract.AbstractAggregation):
    def __init__(self, name, field):
        """
        @param name: the name of this aggregation
        @type name: str
        @param field: the field on which to perform this aggregation
        @type field: str
        """
        super(GeohashGrid, self).__init__(name)
        self.set_field(field)

    def set_field(self, field):
        """
        Set the field for this aggregation
        @param field: the name of the document field on which to perform this aggregation
        @type field: str
        @return:
        @rtype: GeohashGrid
        """
        return self.set_param("field", field)

    def set_precision(self, precision):
        """
        Set the precision for this aggregation
        @param precision: an integer between 1 and 12, inclusive. Defaults to 5.
        @type precision: int
        @return:
        @rtype: GeohashGrid
        """
        return self.set_param("precision", precision)

    def set_size(self, size):
        """
        Set the maximum number of buckets to return
        @param size: defaults to 10,000
        @type size: int
        @return:
        @rtype: GeohashGrid
        """
        return self.set_param("size", size)

    def set_shard_size(self, shard_size):
        """
        Set the number of results returned from each shard
        @param shard_size:
        @type shard_size: int
        @return:
        @rtype: GeohashGrid
        """
        return self.set_param("shard_size", shard_size)