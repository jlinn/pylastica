__author__ = 'Joe Linn'

import abc
from .action import Action
from pylastica.document import Document
from pylastica.script import Script


class AbstractDocument(Action):
    __metaclass__ = abc.ABCMeta

    def __init__(self, document):
        """

        @param document:
        @type document: pylastica.document.Document or pylastica.script.Script
        """
        super(AbstractDocument, self).__init__()
        self.data = document

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

    @property
    def script(self):
        """

        @return:
        @rtype: pylastica.script.Script
        """
        if not isinstance(self._data, Script):
            raise TypeError("This action does not contain a Script: %r" % self._data)
        return self._data

    @script.setter
    def script(self, script):
        """

        @param script:
        @type script: pylastica.script.Script
        """
        self.set_script(script)

    def set_script(self, script):
        """

        @param script:
        @type script: pylastica.script.Script
        @return:
        @rtype: self
        """
        if not isinstance(script, Script):
            raise TypeError("script must be an instance of Script: %r" % script)
        # elif self.op_type != self.OP_TYPE_UPDATE:
        #     raise NotImplementedError("scripts may only be set when performing an update operation: %r" % self.op_type)
        self._data = script
        metadata = self._get_metadata_by_script(script)
        self.metadata = metadata
        return self

    def set_document(self, document):
        """

        @param document:
        @type document: pylastica.document.Document
        @return:
        @rtype: self
        """
        import pylastica.document
        assert isinstance(document, pylastica.document.Document), "document must be an instance of Document: %r" % document
        self._data = document
        metadata = self._get_metadata_by_document(document)
        self.metadata = metadata
        return self

    def get_document(self):
        """

        @return:
        @rtype: pylastica.document.Document
        """
        if not isinstance(self._data, Document):
            raise TypeError("This action does not contain a Document: %r" % self._data)
        return self._data

    def set_data(self, data):
        """

        @param data:
        @type data: pylastica.document.Document or pylastica.script.Script
        @return:
        @rtype: self
        """
        if isinstance(data, Script):
            self.script = data
        elif isinstance(data, Document):
            self.document = data
        else:
            raise TypeError("data must be of type Document or Script: %r" % data)
        return self

    def get_data(self):
        """

        @return:
        @rtype: pylastica.document.Document or pylastica.script.Script
        """
        return self._data

    @property
    def data(self):
        """

        @return:
        @rtype: pylastica.document.Document or pylastica.script.Script
        """
        return self.get_data()

    @data.setter
    def data(self, data):
        """

        @param data:
        @type data: pylastica.document.Document or pylastica.script.Script
        """
        self.set_data(data)

    @abc.abstractmethod
    def _get_metadata_by_document(self, document):
        """

        @param document:
        @type document: pylastica.document.Document
        @return:
        @rtype: dict
        """
        pass

    def _get_metadata_by_script(self, script):
        """

        @param script:
        @type script: pylastica.script.Script
        @return:
        @rtype: dict
        """
        pass

    @classmethod
    def create(cls, data, op_type=None):
        """

        @param cls:
        @type cls:
        @param data:
        @type data: pylastica.document.Document or pylastica.script.Script
        @param op_type: bulk operation type
        @type op_type: str
        @return:
        @rtype: cls
        """
        if not isinstance(data, Document) and not isinstance(data, Script):
            raise TypeError("data must be an instance of Document or Script: %r" % data)
        if op_type is None and data.has_op_type():
            op_type = data.op_type
        if isinstance(data, Script) and op_type is not None and op_type != cls.OP_TYPE_UPDATE:
            raise TypeError("Scripts may only be used for updates.")

        if op_type == cls.OP_TYPE_DELETE:
            from .deletedocument import DeleteDocument
            action = DeleteDocument(data)
        elif op_type == cls.OP_TYPE_CREATE:
            from .createdocument import CreateDocument
            action = CreateDocument(data)
        elif op_type == cls.OP_TYPE_UPDATE:
            from .updatedocument import UpdateDocument
            action = UpdateDocument(data)
        else:
            from .indexdocument import IndexDocument
            action = IndexDocument(data)
        return action
