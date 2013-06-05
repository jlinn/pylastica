__author__ = 'Joe Linn'

from .abstractdocument import AbstractDocument


class DeleteDocument(AbstractDocument):
    def __init__(self, document):
        super(DeleteDocument, self).__init__(document)
        self._op_type = self.OP_TYPE_DELETE

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
