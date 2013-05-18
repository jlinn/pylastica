__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter

class Terms(AbstractFilter):
    def __init__(self, key='', terms=None):
        """

        @param key: document field
        @type key: str
        @param terms: list of term values
        @type terms: list of str
        """
        super(Terms, self).__init__()
        self.set_terms(key, terms)

    def set_terms(self, key, terms):
        """
        Set key and terms for the filter
        @param key: document field
        @type key: str
        @param terms: term values
        @type terms: list of str
        @return:
        @rtype: self
        """
        if not isinstance(terms, list):
            raise TypeError("terms must be a list: %r" % terms)
        self._key = key
        self._terms = terms
        return self

    def add_term(self, term):
        """
        Add a term to the filter
        @param term:
        @type term: str
        @return:
        @rtype: self
        """
        self._terms.append(term)
        return self

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        if not self._key:
            raise pylastica.exception.InvalidException("Terms key must be set!")
        self._params[self._key] = self._terms
        return {'terms': self._params}

