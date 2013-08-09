__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter
import pylastica.exception

class Bool(AbstractFilter):
    def __init__(self):
        self._boost = 1.0
        self._must = []
        self._should = []
        self._must_not = []
        super(Bool, self).__init__()

    def add_should(self, args):
        """
        Add should filter
        @param args:
        @type args: dict or pylastica.filter.AbstractFilter
        @return:
        @rtype: self
        """
        return self._add_filter('should', args)

    def add_must(self, args):
        """
        Add must filter
        @param args:
        @type args: class AbstractFilter(pylastica.param.Param):
        @return:
        @rtype: self
        """
        return self._add_filter('must', args)

    def add_must_not(self, args):
        """
        Add mustNot filter
        @param args:
        @type args: class AbstractFilter(pylastica.param.Param):
        @return:
        @rtype: self
        """
        return self._add_filter('must_not', args)

    def _add_filter(self, type, args):
        """
        Add a general filter based on type
        @param type: filter type
        @type type: str
        @param args:
        @type args: dict or pylastica.filter.AbstractFilter
        @return:
        @rtype: self
        """
        if isinstance(args, pylastica.filter.abstractfilter.AbstractFilter):
            args = args.to_dict()
        assert isinstance(args, dict), "Invalid parameter. Must be a dict or instance of implementation of AbstractFilter."
        var_name = '_' + type
        self.__dict__[var_name].append(args)
        return self

    def to_dict(self):
        args = {
            'bool': {}
        }
        if len(self._must):
            args['bool']['must'] = self._must
        if len(self._should):
            args['bool']['should'] = self._should
        if len(self._must_not):
            args['bool']['must_not'] = self._must_not
        return args

    def set_boost(self, boost):
        """
        Set the boost for this filter
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        self._boost = float(boost)
        return self
