__author__ = 'Joe Linn'

from .abstract import AbstractQuery
import pylastica.doc_type


class Ids(AbstractQuery):
    def __init__(self, doc_type=None, ids=None):
        """
        @param doc_type: document type
        @type doc_type: str or pylastica.doc_type.DocType
        @param ids: document ids
        @type ids: list of str
        """
        super(Ids, self).__init__()
        if doc_type is not None:
            self.set_type(doc_type)
        if ids is not None:
            self.set_ids(ids)

    def add_id(self, doc_id):
        """
        Add another id to the query
        @param doc_id:
        @type doc_id: str
        @return:
        @rtype: self
        """
        if 'values' not in self._params or self._params['values'] is None:
            self._params['values'] = []
        self._params['values'].append(doc_id)
        return self

    def add_type(self, doc_type):
        """
        Add a document type to the query
        @param doc_type:
        @type doc_type: str or pylastica.doc_type.DocType
        @return:
        @rtype: self
        """
        if isinstance(doc_type, pylastica.doc_type.DocType):
            doc_type = doc_type.name
        elif doc_type == '':
            raise pylastica.exception.InvalidException("Document types cannot be empty strings.")
        if 'type' not in self._params or self._params['type'] is None:
            self._params['type'] = []
        self._params['type'].append(doc_type)
        return self

    def set_type(self, doc_type):
        """
        Set the doc type for this query. Overwrites all current values.
        @param doc_type:
        @type doc_type: str or pylastica.doc_type.DocType
        @return:
        @rtype: self
        """
        if isinstance(doc_type, pylastica.doc_type.DocType):
            doc_type = doc_type.name
        elif doc_type == '':
            raise pylastica.exception.InvalidException("Document types cannot be empty strings.")
        self._params['type'] = [doc_type]
        return self

    def set_ids(self, ids):
        """
        Set document ids. Overwrites all current values.
        @param ids:
        @type ids: list of str
        @return:
        @rtype: self
        """
        assert isinstance(ids, list), "ids must be a list: %r" % ids
        self._params['values'] = ids
        return self

