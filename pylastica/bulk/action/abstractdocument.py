__author__ = 'Joe Linn'

import abc
from .action import Action


class AbstractDocument(Action):
    __metaclass__ = abc.ABCMeta

    def __init__(self, document):
        """

        @param document:
        @type document: pylastica.document.Document
        """
        super(AbstractDocument, self).__init__()
        self.document = document

    @property
    def document(self):
        """

        @return:
        @rtype: pylastica.document.Document
        """
        return self.get_document()

    @document.setter
    def document(self, document):
        """

        @param document:
        @type document: pylastica.document.Document
        """
        self.set_document(document)

    def set_document(self, document):
        """

        @param document:
        @type document: pylastica.document.Document
        @return:
        @rtype: self
        """
        import pylastica.document
        assert isinstance(document, pylastica.document.Document), "document must be an instance of Document: %r" % document
        self._document = document
        metadata = self._get_metadata_by_document(document)
        self.metadata = metadata
        return self

    def get_document(self):
        """

        @return:
        @rtype: pylastica.document.Document
        """
        return self._document

    @abc.abstractmethod
    def _get_metadata_by_document(self, document):
        """

        @param document:
        @type document: pylastica.document.Document
        @return:
        @rtype: dict
        """
        pass

    @classmethod
    def create(cls, document, op_type=None):
        """

        @param cls:
        @type cls:
        @param document:
        @type document: pylastica.document.Document
        @param op_type: bulk operation type
        @type op_type: str
        @return:
        @rtype: cls
        """
        import pylastica.document
        assert isinstance(document, pylastica.document.Document), "document must be an instance of Document: %r" % document
        if op_type is None and document.has_op_type():
            op_type = document.op_type
        if op_type == cls.OP_TYPE_DELETE:
            from .deletedocument import DeleteDocument
            action = DeleteDocument(document)
        elif op_type == cls.OP_TYPE_CREATE:
            from .createdocument import CreateDocument
            action = CreateDocument(document)
        elif op_type == cls.OP_TYPE_UPDATE:
            from .updatedocument import UpdateDocument
            action = UpdateDocument(document)
        else:
            from .indexdocument import IndexDocument
            action = IndexDocument(document)
        return action
