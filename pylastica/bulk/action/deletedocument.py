__author__ = 'Joe Linn'

#import pylastica
import pylastica.bulk.action

class DeleteDocument(pylastica.bulk.action.AbstractDocument):
    def __init__(self, document):
        self._op_type = self.OP_TYPE_DELETE
        super(DeleteDocument, self).__init__(document)

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
            'parent'
        ]
        return document.get_options(params, True)
