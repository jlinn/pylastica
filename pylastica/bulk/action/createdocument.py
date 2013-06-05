__author__ = 'Joe Linn'

from .indexdocument import IndexDocument


class CreateDocument(IndexDocument):
    def __init__(self, document):
        super(CreateDocument, self).__init__(document)
        self._op_type = self.OP_TYPE_CREATE
