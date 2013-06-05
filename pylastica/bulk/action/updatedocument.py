__author__ = 'Joe Linn'

from .indexdocument import IndexDocument


class UpdateDocument(IndexDocument):
    def __init__(self, document):
        """

        @param document:
        @type document: pylastica.document.Document
        """
        super(UpdateDocument, self).__init__(document)
        self._op_type = self.OP_TYPE_UPDATE

    @property
    def document(self):
        """

        @return:
        @rtype: pylastica.document.Document
        """
        return super(UpdateDocument, self).document

    @document.setter
    def document(self, document):
        """
        Set the document for this bulk update operation.
        @param document: If the given Document object has a script, the script will be used in the update operation.
        @type document:  pylastica.document.Document
        """
        super(UpdateDocument, self).set_document(document)
        if document.has_script():
            self.source = document.script.to_dict()
            if document.data is not None:
                self.source['upsert'] = document.data
        else:
            self.source = {'doc': document.data}