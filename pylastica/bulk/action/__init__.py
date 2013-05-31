__author__ = 'Joe Linn'

import abc
import json
import pylastica.index


class Action(object):
    OP_TYPE_CREATE = 'create'
    OP_TYPE_INDEX = 'index'
    OP_TYPE_DELETE = 'delete'
    #OP_TYPE_UPDATE = 'update'

    def __init__(self, op_type=OP_TYPE_INDEX, metadata=None, source=None):
        """

        @param op_type: see OP_TYPE_* class properties for options
        @type op_type: str
        @param metadata:
        @type metadata: dict
        @param source:
        @type source: dict
        """
        self.op_type = op_type
        self.metadata = metadata
        self.source = source

    @property
    def op_type(self):
        """

        @return:
        @rtype: str
        """
        return self._op_type

    @op_type.setter
    def op_type(self, op_type):
        """

        @param op_type: see OP_TYPE_* class properties for options
        @type op_type: str
        """
        self._op_type = op_type

    @property
    def metadata(self):
        """

        @return:
        @rtype: dict
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """

        @param metadata:
        @type metadata: dict
        """
        if metadata is None:
            metadata = {}
        self._metadata = metadata

    @property
    def action_metadata(self):
        """

        @return:
        @rtype: dict
        """
        return {self.op_type: self.metadata}

    @property
    def source(self):
        """

        @return:
        @rtype: dict
        """
        return self._source

    @source.setter
    def source(self, source):
        """

        @param source:
        @type source: dict
        """
        self._source = source

    def has_source(self):
        """

        @return:
        @rtype: bool
        """
        return self._source is not None

    def set_index(self, index):
        """

        @param index:
        @type index: str or pylastica.index.Index
        @return:
        @rtype: self
        """
        if isinstance(index, pylastica.index.Index):
            index = index.name
        self._metadata['_index'] = index
        return self

    def set_type(self, doc_type):
        """

        @param doc_type:
        @type doc_type: str or pylastica.doc_type.DocType
        @return:
        @rtype: self
        """
        if isinstance(doc_type, pylastica.doc_type.DocType):
            self.set_index(doc_type.index.name)
            doc_type = doc_type.name
        self._metadata['_type'] = type
        return self

    def set_id(self, doc_id):
        """

        @param doc_id:
        @type doc_id: str
        @return:
        @rtype: self
        """
        self._metadata['_id'] = doc_id
        return self

    def to_list(self):
        """

        @return:
        @rtype: list
        """
        data = [self.action_metadata]
        if self.has_source():
            data.append(self.source)
        return data

    def to_string(self):
        """

        @return:
        @rtype: str
        """
        from pylastica.bulk import Bulk
        string = json.dumps(self.action_metadata) + Bulk.DELIMITER
        if self.has_source():
            source = self.source
            if isinstance(source, str):
                string += source
            else:
                string += json.dumps(source)
            string += Bulk.DELIMITER
        return string

    def __str__(self):
        """

        @return:
        @rtype: str
        """
        return self.to_string()

    @staticmethod
    def is_valid_op_type(op_type):
        """
        Determines whether or not the given op type is a valid bulk operation
        @param op_type:
        @type op_type: str
        @return:
        @rtype: bool
        """
        valid = [
            pylastica.bulk.action.Action.OP_TYPE_INDEX,
            pylastica.bulk.action.Action.OP_TYPE_CREATE,
            pylastica.bulk.action.Action.OP_TYPE_DELETE
        ]
        return op_type in valid


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
        assert isinstance(document, pylastica.document.Document), "document must be an instance of Document: %r" % document
        if op_type is None and document.has_op_type():
            op_type = document.op_type
        if op_type == cls.OP_TYPE_DELETE:
            action = DeleteDocument(document)
        elif op_type == cls.OP_TYPE_CREATE:
            action = CreateDocument(document)
        else:
            action = IndexDocument(document)
        return action


class IndexDocument(AbstractDocument):
    def __init__(self, document):
        super(IndexDocument, self).__init__(document)
        self._op_type = self.OP_TYPE_INDEX

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


class CreateDocument(IndexDocument):
    def __init__(self, document):
        super(CreateDocument, self).__init__(document)
        self._op_type = self.OP_TYPE_CREATE


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
