__author__ = 'Joe Linn'

import pylastica.aggregation.abstractaggregation as abstract


class Terms(abstract.SimpleAggregation):
    """
    Terms Aggregation
    @see http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-aggregations-bucket-terms-aggregation.html
    """
    def set_order(self, order, direction):
        """
        Set the bucket sort order
        @param order: _count, _term, or the name of a sub-aggregation or sub-aggregation response field
        @type order: str
        @param direction: asc or desc
        @type direction: str
        @return:
        @rtype: Terms
        """
        return self.set_param('order', {order: direction})

    def set_minimum_document_count(self, count):
        """
        Set the minimum number of documents in which a term must appear in order to be returned in a bucket
        @param count:
        @type count: int
        @return:
        @rtype: Terms
        """
        return self.set_param('min_doc_count', count)

    def set_include(self, pattern, flags=None):
        """
        Filter documents to include based on a regular expression
        @param pattern:
        @type pattern: str
        @param flags: Java Pattern flags
        @type flags: str
        @return:
        @rtype: Terms
        """
        if flags is None:
            return self.set_param("include", pattern)
        return self.set_param("include", {
            "pattern": pattern,
            "flags": flags
        })

    def set_exclude(self, pattern, flags=None):
        """
        Filter documents to exclude based on a regular expression
        @param pattern:
        @type pattern: str
        @param flags: Java Pattern flags
        @type flags: str
        @return:
        @rtype: Terms
        """
        if flags is None:
            return self.set_param("exclude", pattern)
        return self.set_param("exclude", {
            "pattern": pattern,
            "flags": flags
        })

    def set_execution_hint(self, hint):
        """
        Direct Elasticsearch to use direct field data or ordinals of the field values to execute this aggregation.
        The execution hint will be ignored if it is not applicable.
        @param hint: map or ordinals
        @type hint: str
        @return:
        @rtype: Terms
        """
        return self.set_param("execution_hint", hint)

    def set_size(self, size):
        """
        Define how many term buckets should be returned
        @param size:
        @type size: int
        @return:
        @rtype: Terms
        """
        return self.set_param("size", size)

    def set_shard_size(self, shard_size):
        """
        Determines how many terms the coordinating node will request from each shard.
        @param shard_size: This number cannot be smaller than the "size" parameter
        @type shard_size: int
        @return:
        @rtype: Terms
        """
        return self.set_param("shard_size", shard_size)