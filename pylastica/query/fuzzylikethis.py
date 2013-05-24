__author__ = 'Joe Linn'

from .abstract import AbstractQuery

class FuzzyLikeThis(AbstractQuery):
    def __init__(self):
        super(FuzzyLikeThis, self).__init__()
        self._fields = []
        self._like_text = ''
        self._ignore_tf = False
        self._max_query_terms = 25
        self._min_similarity = 0.5
        self._prefix_length = 0
        self._boost = 1.0

    def set_fields(self, fields):
        """
        Set fields for this query
        @param fields: field names
        @type fields: list of str
        @return:
        @rtype: self
        """
        self._fields = fields
        return self

    def set_like_text(self, text):
        """
        Set the like_text value
        @param text:
        @type text: str
        @return:
        @rtype: self
        """
        self._like_text = text.strip()
        return self

    def set_ignore_tf(self, ignore=True):
        """
        Set the ignore_tf (term frequency) value
        @param ignore:
        @type ignore: bool
        @return:
        @rtype: self
        """
        self._ignore_tf = bool(ignore)
        return self

    def set_min_similarity(self, value):
        """
        Set the minimum similarity
        @param value:
        @type value: float
        @return:
        @rtype: self
        """
        self._min_similarity = float(value)
        return self

    def set_boost(self, boost):
        """
        Set the boost for this query
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        self._boost = float(boost)
        return self

    def set_prefix_length(self, value):
        """
        Set the prefix length
        @param value:
        @type value: int
        @return:
        @rtype: self
        """
        self._prefix_length = int(value)
        return self

    def set_max_query_terms(self, terms):
        """
        Set the max_query_terms
        @param terms:
        @type terms: int
        @return:
        @rtype: self
        """
        self._max_query_terms = int(terms)
        return self

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        args = {}
        if len(self._fields):
            args['fields'] = self._fields
        if self._boost is not None:
            args['boost'] = self._boost
        if self._like_text:
            args['like_text'] = self._like_text
        args['min_similarity'] = self._min_similarity if self._min_similarity > 0 else 0
        args['prefix_length'] = self._prefix_length
        args['ignore_tf'] = self._ignore_tf
        args['max_query_terms'] = self._max_query_terms
        return {'fuzzy_like_this': args}
