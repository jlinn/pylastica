__author__ = 'Joe Linn'

from .abstract import AbstractQuery
import pylastica.exception


class Terms(AbstractQuery):
    def __init__(self, key='', terms=None):
        """
        Construct terms query
        @param key: terms key
        @type key: str
        @param terms: terms list
        @type terms: list
        """
        super(Terms, self).__init__()
        self.set_terms(key, terms)

    def set_terms(self, key, terms):
        """
        Set key and terms for the query
        @param key:
        @type key: str
        @param terms:
        @type terms: list
        @return:
        @rtype: self
        """
        self._key = key
        if terms is None:
            terms = []
        self._terms = terms
        return self

    def add_term(self, term):
        """
        Add a single term to the list
        @param term:
        @type term: str
        @return:
        @rtype: self
        """
        self._terms.append(term)
        return self

    def set_minimum_match(self, minimum):
        """
        Set the minimum matching value
        @param minimum:
        @type minimum: int
        @return:
        @rtype: self
        """
        return self.set_param('minimum_match', minimum)

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        if self._key is None:
            raise pylastica.exception.InvalidException("Terms key must be set.")
        self.set_param(self._key, self._terms)
        return super(Terms, self).to_dict()
