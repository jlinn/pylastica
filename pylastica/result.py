__author__ = 'Joe Linn'

class Result(object):
    def __init__(self, hit):
        """

        @param hit:
        @type hit: dict
        @return:
        """
        self._hit = hit

    def get_param(self, name):
        """
        Return a param from the result hit dict
        @param name:
        @type name: str
        @return:
        @rtype: dict
        """
        if name in self._hit:
            return self._hit[name]
        return {}

    def get_id(self):
        """
        Returns the hit id
        @return:
        @rtype: str
        """
        return self.get_param('_id')

    def get_type(self):
        """
        Return the type of the result
        @return:
        @rtype: str
        """
        return self.get_param('_type')

    def get_fields(self):
        """
        Returns a list of fields
        @return:
        @rtype: dict
        """
        return self.get_param('fields')

    def get_index(self):
        """
        Returns the index name of the result
        @return:
        @rtype: str
        """
        return self.get_param('_index')

    def get_score(self):
        """
        Return the score of the result
        @return:
        @rtype: float
        """
        return self.get_param('_score')

    def get_hit(self):
        """
        Return the raw hit dict
        @return:
        @rtype: dict
        """
        return self._hit

    def get_version(self):
        """
        Return the version of the hit
        @return:
        @rtype: int
        """
        return self.get_param('_version')

    @property
    def data(self):
        """
        Returns result data
        @return:
        @rtype: dict
        """
        return self.get_data()

    def get_data(self):
        """
        Returns result data
        @return:
        @rtype: dict
        """
        if 'fields' in self._hit and '_source' not in self._hit:
            return self.get_fields()
        else:
            return self.get_source()

    def get_source(self):
        """
        Return the result source
        @return:
        @rtype: dict
        """
        return self.get_param('_source')

    def get_highlights(self):
        """
        Return result data
        @return:
        @rtype: dict
        """
        return self.get_param('highlight')

    def get_explanation(self):
        """
        Return an explanation of how the result's score was computed
        @return:
        @rtype: dict
        """
        return self.get_param('_explanation')

    # def __getattribute__(self, name):
    #     source = self.get_data()
    #     if name in source:
    #         return source[name]
    #     else:
    #         return None


