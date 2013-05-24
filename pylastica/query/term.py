__author__ = 'Joe Linn'

from .abstract import AbstractQuery

class Term(AbstractQuery):
    def __init__(self, term=None):
        """

        @param term: optional
        @type term: dict
        """
        super(Term, self).__init__()
        if term is not None:
            self.set_raw_term(term)

    def set_raw_term(self, term):
        """
        Set term.
        @param term:
        @type term: dict
        @return:
        @rtype: self
        """
        self.params = term
        return self

    def set_term(self, key, value, boost=1.0):
        """
        Add a term to the query
        @param key: key to query
        @type key: str
        @param value: value(s) for the query
        @type value: str or list
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        return self.set_raw_term({key: {'value': value, 'boost': boost}})
