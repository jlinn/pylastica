__author__ = 'Joe Linn'

#import pylastica
import pylastica.bulk.action.abstractdocument

class IndexDocument(pylastica.bulk.action.abstractdocument.AbstractDocument):
    def __init__(self, document):
        self._op_type = self.OP_TYPE_INDEX
        super(IndexDocument, self).__init__(document)

    @property
    def document(self):
        """

        @return:
        @rtype: pylastica.document.Document
        """
        return super(IndexDocument, self).document

    @document.setter
    def document(self, document):
        """
        @param document:
        @type document:  pylastica.document.Document
        """
        super(IndexDocument, self).set_document(document)
        self.source = document.data

    def _get_metadata_by_document(self, document):
        """

        @param document:
        @type document: pylastica.document.Document
        @return:
        @rtype: dict
        """
        params = [
            'index',
            'type',
            'id',
            'version',
            'version_type',
            'routing',
            'percolate',
            'parent',
            'ttl',
            'timestamp'
        ]
        metadata = document.get_options(params, True)
        return metadata
