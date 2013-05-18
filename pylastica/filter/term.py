__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter

class Term(AbstractFilter):
    def __init__(self, field=None, value=None):
        """

        @param field: document field
        @type field: str
        @param value:
        @type value: str or dict
        """
        super(Term, self).__init__()
        if field is not None:
            self.set_raw_term({field: value})

    def set_raw_term(self, term):
        """
        Set / overwrite key and term
        @param term: {field: value}
        @type term: dict
        @return:
        @rtype: self
        """
        self.params = term
        return self

    def set_term(self, field, value):
        """
        Set the term for the filter
        @param field: document field
        @type field: str
        @param value: value for the filter
        @type value: str
        @return:
        @rtype: self
        """
        return self.set_raw_term({field: value})
