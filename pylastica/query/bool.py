__author__ = 'Joe Linn'

from .abstract import AbstractQuery
import pylastica.exception

class Bool(AbstractQuery):
    def add_should(self, args):
        """
        Add should part to query
        @param args:
        @type args: pylastica.query.AbstractQuery or dict
        @return:
        @rtype: self
        """
        return self._add_query('should', args)

    def add_must(self, args):
        """
        Add must part to the query
        @param args:
        @type args: pylastica.query.AbstractQuery or dict
        @return:
        @rtype: self
        """
        return self._add_query('must', args)

    def add_must_not(self, args):
        """
        Add must not part
        @param args:
        @type args: pylastica.query.AbstractQuery or dict
        @return:
        @rtype: self
        """
        return self._add_query('must_not', args)

    def _add_query(self, type, args):
        """
        Adds a query to the current object
        @param type: query type
        @type type: str
        @param args: query
        @type args: pylastica.query.AbstractQuery or dict
        @return:
        @rtype: bool
        """
        if isinstance(args, AbstractQuery):
            args = args.to_dict()
        assert isinstance(args, dict), "Invalid parameter. Must be array or instance of pylastica.query.AbstractQuery: %r" % args
        return self.add_param(type, args)

    def set_boost(self, boost):
        """
        Set the boost value of this query
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        return self.set_param('boost', boost)

    def set_minimum_number_should_match(self, minimum):
        """
        Set the minimum number of docs which should match this query
        @param minimum:
        @type minimum: int
        @return:
        @rtype: self
        """
        return self.set_param('minimum_number_should_match', minimum)
