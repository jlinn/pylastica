__author__ = 'Joe Linn'

from .abstract import AbstractQuery
import pylastica.script

class CustomScore(AbstractQuery):
    def __init__(self, script=None, query=None):
        """

        @param script:
        @type script: str or dict or pylastica.script.Script
        @param query:
        @type query: str or pylastica.query.AbstractQuery
        """
        super(CustomScore, self).__init__()
        if script is not None:
            self.set_script(script)
        self.set_query(query)

    def set_query(self, query):
        """
        Set the query object
        @param query:
        @type query: str or pylastica.query.Query or pylastica.query.AbstractQuery
        @return:
        @rtype: self
        """
        query = pylastica.query.Query.create(query)
        data = query.to_dict()
        return self.set_param('query', data['query'])

    def set_script(self, script):
        """
        Set the script
        @param script:
        @type script: str or pylastica.script.Script or dict
        @return:
        @rtype: self
        """
        script = pylastica.script.Script.create(script)
        for param, value in script.to_dict().iteritems():
            self.set_param(param, value)
        return self

    def add_params(self, params):
        """
        Add params for the script
        @param params:
        @type params: dict
        @return:
        @rtype: self
        """
        return self.set_param('params', params)
