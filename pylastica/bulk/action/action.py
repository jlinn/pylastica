__author__ = 'Joe Linn'

import json
import pylastica.index


class Action(object):
    OP_TYPE_CREATE = 'create'
    OP_TYPE_INDEX = 'index'
    OP_TYPE_DELETE = 'delete'
    OP_TYPE_UPDATE = 'update'

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
            Action.OP_TYPE_INDEX,
            Action.OP_TYPE_CREATE,
            Action.OP_TYPE_DELETE,
            Action.OP_TYPE_UPDATE
        ]
        return op_type in valid

