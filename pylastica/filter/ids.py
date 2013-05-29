__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
import pylastica.doc_type
from .abstractfilter import AbstractFilter

class Ids(AbstractFilter):
    def __init__(self, doc_type=None, ids=None):
        """

        @param doc_type: document type
        @type doc_type: str or pylastica.doc_type.DocType
        @param ids: list of document ids
        @type ids: list of str or str
        """
        super(Ids, self).__init__()
        self.set_doc_type(doc_type)
        self.set_ids(ids)

    def add_id(self, doc_id):
        """
        Add a document id to the filter
        @param id: document id
        @type id: str
        @return:
        @rtype: self
        """
        return self.add_param('values', doc_id)

    def add_doc_type(self, doc_type):
        """
        Add another document type to the filter
        @param doc_type: document type
        @type doc_type: str or pylastica.doc_type.DocType
        @return:
        @rtype: self
        """
        if isinstance(doc_type, pylastica.doc_type.DocType):
            doc_type = doc_type.name
        return self.add_param('type', doc_type)

    def set_doc_type(self, doc_type):
        """
        Set the document type
        @param doc_type: doc type
        @type doc_type: str or pylastica.doc_type.DocType or list of str
        @return:
        @rtype: self
        """
        if isinstance(doc_type, pylastica.doc_type.DocType):
            doc_type = doc_type.name
        return self.set_param('type', doc_type)

    def set_ids(self, ids):
        """
        Set document ids for the filter
        @param ids:
        @type ids: list of str or str
        @return:
        @rtype: self
        """
        if not isinstance(ids, list):
            ids = [ids]
        return self.set_param('values', ids)
