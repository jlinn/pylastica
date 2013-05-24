__author__ = 'Joe Linn'

#import pylastica
from .abstract import AbstractQuery

class CustomFiltersScore(AbstractQuery):
    SCORE_MODE_FIRST = 'first'
    SCORE_MODE_MIN = 'min'
    SCORE_MODE_MAX = 'max'
    SCORE_MODE_TOTAL = 'total'
    SCORE_MOD_AVG = 'avg'
    SCORE_MODE_MULTIPLY = 'multiply'

    def __init__(self, query=None):
        """

        @param query:
        @type query: dict or pylastica.query.Query
        """
        super(CustomFiltersScore, self).__init__()
        self.set_query(query)

    def set_query(self, query):
        """
        Set the query
        @param query:
        @type query: pylastica.query.Query or dict
        @return:
        @rtype: self
        """
        query = pylastica.query.Query.create(query)
        data = query.to_dict()
        self.set_param('query', data['query'])
        return self

    def add_filter(self, filter, boost):
        """
        Add a filter with boost
        @param filter:
        @type filter: pylastica.filter.AbstractFilter
        @param boost: boost for the filter
        @type boost: float
        @return:
        @rtype: self
        """
        assert isinstance(filter, pylastica.filter.AbstractFilter), "filter must be a descendant of AbstractFilter: %r" % filter
        filter_param = {
            'filter': filter.to_dict(),
            'boost': boost
        }
        return self.add_param('filters', filter_param)

    def add_filter_script(self, filter, script):
        """
        Add a filter with a script to calculate the score.
        @param filter: filter object
        @type filter: pylastica.filter.AbstractFilter
        @param script:
        @type script: pylastica.script.Script or str or dict
        @return:
        @rtype: self
        """
        assert isinstance(filter, pylastica.filter.AbstractFilter), "filter must be a descendant of AbstractFilter: %r" % filter
        script = pylastica.script.Script.create(script)
        filter_param = {
            'filter': filter.to_dict(),
            'script': script.script
        }
        return self.add_param('filters', filter_param)

    def set_script_lang(self, lang):
        """
        Set language for scripts in filters
        @param lang:
        @type lang: str
        @return:
        @rtype: self
        """
        return self.set_param('lang', lang)

    def set_script_params(self, params):
        """
        Set parameters for scripts
        @param params:
        @type params: dict
        @return:
        @rtype: self
        """
        return self.set_param('params', params)

    def set_score_mode(self, score_mode):
        """
        Set the score mode.
        @param score_mode: See SCORE_MODE_* class properties for options.
        @type score_mode: str
        @return:
        @rtype: self
        """
        return self.set_param('score_mode', score_mode)
