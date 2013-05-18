__author__ = 'Joe Linn'

#import pylastica.filter.abstractfilter
from .abstractfilter import AbstractFilter

class DocType(AbstractFilter):
    def __init__(self, type_name=None):
        """
        @param type_name: document type name
        @type type_name: str
        """
        super(DocType, self).__init__()
        if type_name is not None:
            self.set_doc_type(type_name)


    def set_doc_type(self, type_name):
        """
        Set the document type
        @param type_name:
        @type type_name: str
        @return:
        @rtype: self
        """
        self._type = type_name
        return self

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        return {
            'type': {'value': self._type}
        }

