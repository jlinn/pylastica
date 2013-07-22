__author__ = 'Joe Linn'

from . import action
from .action import abstractdocument
from .response import *
from .responseset import *
import pylastica.exception.bulk


class Bulk(object):
    DELIMITER = "\n"
    UDP_DEFAULT_HOST = 'localhost'
    UDP_DEFAULT_PORT = 9700

    def __init__(self, client):
        """

        @param client:
        @type client: pylastica.client.Client
        """
        assert isinstance(client, pylastica.client.Client), "client must be an instance of Client: %r" % client
        self._client = client
        self._actions = []
        self._index = ''
        self._type = ''

    @property
    def index(self):
        """
        The name of the index to be used for this operation
        @return:
        @rtype: str
        """
        return self._index

    @index.setter
    def index(self, index):
        """
        Set the index to be used for this operation
        @param index:
        @type index: str or pylastica.index.Index
        """
        if isinstance(index, pylastica.index.Index):
            index = index.name
        self._index = str(index)

    def has_index(self):
        """

        @return:
        @rtype: bool
        """
        return self.index is not None and self.index != ''

    @property
    def doc_type(self):
        """
        Return the type name for this operation
        @return:
        @rtype: str
        """
        return self._type

    @doc_type.setter
    def doc_type(self, doc_type):
        """

        @param doc_type:
        @type doc_type: str or pylastica.doc_type.DocType
        """
        if isinstance(doc_type, pylastica.doc_type.DocType):
            self.index = doc_type.index.name
            doc_type = doc_type.name
        self._type = str(doc_type)

    def has_type(self):
        """

        @return:
        @rtype: bool
        """
        return self.doc_type is not None and self.doc_type != ''

    @property
    def path(self):
        """

        @return:
        @rtype: str
        """
        path = '/'
        if self.has_index():
            path += self.index + '/'
            if self.has_type():
                path += self.doc_type + '/'
        path += '_bulk'
        return path

    def add_action(self, action):
        """
        Add a bulk action
        @param action:
        @type action: pylastica.bulk.action.Action
        @return:
        @rtype: self
        """
        assert isinstance(action, pylastica.bulk.action.Action), "action must be an instance of Action: %r" % action
        self._actions.append(action)
        return self

    def add_actions(self, actions):
        """
        Add multiple actions
        @param actions:
        @type actions: list of pylastica.bulk.action.Action
        @return:
        @rtype: self
        """
        for action in actions:
            self.add_action(action)
        return self

    @property
    def actions(self):
        """

        @return:
        @rtype: list of pylastica.bulk.action.Action
        """
        return self._actions

    def add_document(self, document, op_type=None):
        """

        @param document:
        @type document: pylastica.document.Document
        @param op_type: bulk operation type
        @type op_type: str
        @return:
        @rtype: self
        """
        from pylastica.bulk.action import AbstractDocument
        return self.add_action(AbstractDocument.create(document, op_type))

    def add_documents(self, documents, op_type=None):
        """

        @param documents:
        @type documents: list of pylastica.document.Document
        @param op_type: bulk operation type
        @type op_type: str
        @return:
        @rtype: self
        """
        for doc in documents:
            self.add_document(doc, op_type)
        return self

    def add_raw_data(self, data):
        """
        Add raw bulk data according to the ES bulk protocol
        @param data:
        @type data: list of dict
        @return:
        @rtype: self
        """
        bulk_action = None
        for row in data:
            if isinstance(row, dict):
                op_type = row.keys()[0]
                metadata = row[op_type]
                if pylastica.bulk.action.Action.is_valid_op_type(op_type):
                    #add previous action
                    if bulk_action is not None:
                        self.add_action(bulk_action)
                    bulk_action = pylastica.bulk.action.Action(op_type, metadata)
                elif isinstance(bulk_action, pylastica.bulk.action.Action):
                    bulk_action.source = row
                    self.add_action(bulk_action)
                    bulk_action = None
                else:
                    raise pylastica.exception.InvalidException("Invalid bulk data. Source must follow action metadata.")
            else:
                raise pylastica.exception.InvalidException("Invalid bulk data. Should be list of dict, Document, or Bulk.Action")
        #add last action if available
        if bulk_action is not None:
            self.add_action(bulk_action)
        return self

    def add_script(self, script, op_type=None):
        """
        Add a script
        @param script: Script object
        @type script: pylastica.script.Script
        @param op_type: bulk operation
        @type op_type: str
        @return:
        @rtype: self
        """
        action = abstractdocument.AbstractDocument.create(script, op_type)
        return self.add_action(action)

    def add_scripts(self, scripts, op_type=None):
        """
        Add multiple scripts
        @param scripts:
        @type scripts: list of pylastica.script.Script
        @param op_type: bulk operation
        @type op_type: str
        @return:
        @rtype: self
        """
        for script in scripts:
            self.add_script(script)
        return self

    def add_data(self, data, op_type=None):
        """
        Add data (document or script)
        @param data:
        @type data: pylastica.document.Document or pylastica.script.Script or list of pylastica.document.Document or list of pylastica.script.Script
        @param op_type: bulk operation
        @type op_type: str
        @return:
        @rtype: self
        """
        if not isinstance(data, list):
            data = [data]
        for action_data in data:
            if isinstance(action_data, pylastica.script.Script):
                self.add_script(action_data)
            elif isinstance(action_data, pylastica.document.Document):
                self.add_document(action_data)
            else:
                raise TypeError("Data must be a Document, a Script, or a list comprised of either or both of those types: %r" % action_data)
        return self

    def to_string(self):
        """

        @return:
        @rtype: str
        """
        data = ''
        for action in self.actions:
            data += str(action)
        return data

    def __str__(self):
        """

        @return:
        @rtype: str
        """
        return self.to_string()

    def to_list(self):
        """

        @return:
        @rtype: list
        """
        data = []
        for action in self.actions:
            for row in action.to_list():
                data.append(row)
        return data

    def send(self):
        """
        Send this bulk action to the server
        @return:
        @rtype: pylastica.bulk.responseset.ResponseSet
        """
        return self._process_response(self._client.request(self.path, pylastica.request.Request.PUT, str(self)))

    def _process_response(self, response):
        """

        @param response:
        @type response: pylastica.response.Response
        @return:
        @rtype: pylastica.bulk.responseset.ResponseSet
        """
        from pylastica.bulk.action import AbstractDocument
        response_data = response.data
        actions = self.actions
        bulk_responses = []
        if 'items' in response_data and isinstance(response_data['items'], list):
            for key, item in enumerate(response_data['items']):
                try:
                    action = actions[key]
                except ValueError:
                    raise pylastica.exception.InvalidException("No response found for action #%s." % key)
                op_type = action.op_type
                bulk_response_data = item[item.keys()[0]]
                if isinstance(action, AbstractDocument):
                    data = action.get_data()
                    if isinstance(data, pylastica.document.Document) and data.auto_populate or self._client.get_config_value(['document', 'autoPopulate'], False):
                        if not data.has_id() and '_id' in bulk_response_data:
                            data.doc_id = bulk_response_data['_id']
                        if '_version' in bulk_response_data:
                            data.version = bulk_response_data['_version']
                bulk_responses.append(pylastica.bulk.response.Response(bulk_response_data, action, op_type))
        bulk_response_set = pylastica.bulk.responseset.ResponseSet(response, bulk_responses)
        if bulk_response_set.has_error():
            raise pylastica.exception.bulk.ResponseException(bulk_response_set)
        return bulk_response_set

    def send_udp(self, host=None, port=None):
        """

        @param host:
        @type host: str
        @param port:
        @type port: int
        @return:
        @rtype:
        """
        if host is None:
            host = self._client.get_config_value(['udp', 'host'], self.UDP_DEFAULT_HOST)
        if port is None:
            port = self._client.get_config_value(['udp', 'port'], self.UDP_DEFAULT_PORT)
        message = str(self)
        #TODO: implement udp socket stuff
        raise NotImplementedError("Haven't implemented UDP bulk transmission yet.")
