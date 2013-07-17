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
        @param document:
        @type document:  pylastica.document.Document
        """
        super(UpdateDocument, self).set_document(document)
        source = {'doc': document.data}
        if document.doc_as_upsert:
            source['doc_as_upsert'] = True
        elif document.has_upsert():
            upsert = document.upsert.data
            if upsert is not None:
                source['upsert'] = upsert
        self.source = source

    @property
    def script(self):
        """

        @return:
        @rtype: pylastica.script.Script
        """
        return super(UpdateDocument, self).script

    @script.setter
    def script(self, script):
        """

        @param script:
        @type script: pylastica.script.Script
        """
        super(UpdateDocument, self).set_script(script)
        source = script.to_dict()
        if script.has_upsert():
            upsert = script.upsert.data
            if upsert is not None:
                source['upsert'] = upsert
        self.source = source

    def _get_metadata_by_script(self, script):
        """

        @param script:
        @type script: pylastica.script.Script
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
        metadata = script.get_options(params, True)
        return metadata
