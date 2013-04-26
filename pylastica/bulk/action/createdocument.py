__author__ = 'Joe Linn'

import pylastica

class CreateDocument(pylastica.bulk.action.IndexDocument):
    def __init__(self, document):
        super(CreateDocument, self).__init__(document)
        self._op_type = self.OP_TYPE_CREATE
