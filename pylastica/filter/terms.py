__author__ = 'Joe Linn'

import pylastica.exception
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
        if terms is not None:
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

    def set_lookup(self, key, doc_type, id, path, index=None):
        """
        Set the lookup path for this terms filter
        @param key: document field
        @type key: str
        @param doc_type: the document type from which to fetch the term values
        @type doc_type: str or pylastica.doc_type.DocType
        @param id: id of the document from which to fetch the term values
        @type id: str
        @param path: the field specified as path from which to fetch the values for the filter
        @type path: str
        @param index: The index from which to fetch the term values. Defaults to the current index.
        @type index: str or pylastica.index.Index
        @return:
        @rtype: self
        """
        self._key = key
        if isinstance(doc_type, pylastica.doc_type.DocType):
            doc_type = doc_type.name
        self._terms = {
            'type': doc_type,
            'id': id,
            'path': path
        }
        if index is not None:
            if isinstance(index, pylastica.index.Index):
                index = index.name
            self._terms['index'] = index
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

