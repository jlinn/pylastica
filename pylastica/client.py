__author__ = 'Joe Linn'

import pylastica

class Client(object):

    def __init__(self, host=None, port=None, path=None, url=None, transport=None, persistent=True, timeout=None, connections=None, round_robin=False, log=False, retry_on_conflict=0, callback=None):
        """
        @param host:
        @type host: str
        @param port:
        @type port: int
        @param path:
        @type path: str
        @param url:
        @type url: str
        @param transport:
        @type transport:
        @param persistent:
        @type persistent:
        @param timeout:
        @type timeout:
        @param connections:
        @type connections:
        @param round_robin:
        @type round_robin:
        @param log: set to True to enable logging. Set to a string to specify a log file.
        @type log: bool or str
        @param retry_on_conflict: retry document update on conflict
        @type retry_on_conflict: bool
        @param callback:
        @type callback:
        @return:
        @rtype:
        """
        if connections is None:
            connections = []
        self._connections = connections
        self._callback = callback
        """@type: pylastica.response.Response"""
        self._last_response = None
        self._config = {
            'host': host,
            'port': port,
            'path': path,
            'url': url,
            'transport': transport,
            'persistent': persistent,
            'timeout': timeout,
            'connections': connections,
            'round_robin': round_robin,
            'log': log,
            'retry_on_conflict': retry_on_conflict
        }

    def set_config(self, config):
        """
        Set specific config values (updates if values are already set)
        @param config:
        @type config: dict
        @return:
        @rtype: self
        """
        for key, value in config.iteritems():
            self._config[key] = value
        return self

    def get_config(self, key=None):
        """
        Return a specific config value of the whole config dict
        @param key:
        @type key: str
        @return:
        @rtype: str or dict
        """
        if key is None:
            return self._config
        if key not in self._config:
            raise pylastica.exception.InvalidException("Config key is not set: %s" %key)
        return self._config[key]

    def set_config_value(self, key, value):
        """
        Set / overwrite a specific config value
        @param key:
        @type key: str
        @param value:
        @type value: mixed
        @return:
        @rtype: self
        """
        return self.set_config({key: value})

    def get_config_value(self, keys, default=None):
        """

        @param keys: a string to get a single config value, or a list of keys to get multiple config values
        @type keys: list or str
        @param default: default value which will be returned if the key is not found in the config
        @type default: mixed
        @return:
        @rtype: mixed
        """
        value = self._config
        if isinstance(keys, str):
            keys = [keys]
        for key in keys:
            if key in value:
                value = value[key]
            else:
                return default
        return value

    def get_index(self, name):
        """
        Returns an index object for the given index name
        @param name: index name
        @type name: str
        @return:
        @rtype: pylastica.index.Index
        """
        return pylastica.index.Index(self, name)

    def add_header(self, header, header_value):
        """
        Add a HTTP header
        @param header: header key
        @type header: str
        @param header_value: header value
        @type header_value: str
        @return:
        @rtype: self
        """
        if isinstance(header, str) and isinstance(header_value, str):
            self._config['headers'][header] = header_value
            return self
        raise pylastica.exception.InvalidException("header and header_value must be strings.")

    def remove_header(self, header):
        """
        Remove a HTTP header
        @param header: key of header to remove
        @type header: str
        @return:
        @rtype: self
        """
        if isinstance(header, str):
            if header in self._config['headers']:
                del self._config['headers'][header]
            return self
        else:
            raise pylastica.exception.InvalidException("header must be of type str: %r" %header)

    def add_documents(self, docs):
        """
        Uses _bulk to send documents to the server
        @param docs: list of document objects
        @type docs: list of pylastica.document.Document
        @return: bulk response object
        @rtype: pylastica.bulk.responseset.ResponseSet
        """
        assert isinstance(docs, list) and len(docs), "docs must be a list of at least one Document object: %r" % docs
        return pylastica.bulk.Bulk(self).add_documents(docs).send()

    def update_document(self, doc_id, data, index, doc_type, options=None):
        """
        Update a document via an update script
        @param doc_id:  document id
        @type doc_id: str
        @param data: data for request body
        @type data: dict or pylastica.script.Script or pylastica.document.Document
        @param index: index to update
        @type index: str
        @param doc_type: document type
        @type doc_type: str
        @param options: optional dict of query parameters
        @type options: dict
        @return:
        @rtype: pylastica.response.Response
        """
        if options is None:
            options = {}
        path = '/'.join([index, type, id, '_update'])
        if isinstance(data, pylastica.script.Script):
            request_data = data.to_dict()
        elif isinstance(data, pylastica.document.Document):
            if data.has_script():
                request_data = data.script.to_dict()
                document_data = data.data
                if document_data is not None:
                    request_data['upsert'] = document_data
            else:
                request_data = {'doc': data.data}
            doc_options = data.get_options([
                'version',
                'version_type',
                'routing',
                'percolate',
                'parent',
                'fields',
                'retry_on_conflict',
                'consistency',
                'replication',
                'refresh',
                'timeout',
            ])
            options.update(doc_options)
            #set fields param to source only if options was not set before
            if data.auto_populate or self.get_config_value(['document', 'autopopulate'], False) and 'fields' not in options:
                options['fields'] = '_source'
        else:
            request_data = data
        if 'retry_on_conflict' not in options:
            retry_on_conflict = self.get_config('retry_on_conflict')
            options['retry_on_conflict'] = retry_on_conflict
        response = self.request(path, pylastica.request.Request.POST, request_data, options)
        if response.is_ok() and isinstance(data, pylastica.document.Document) and data.auto_populate or self.get_config_value(['document', 'autopopulate'], False):
            response_data = response.data
            if '_version' in response_data:
                data.version = response_data['_version']
            if 'fields' in options:
                self._populate_document_fields_from_response(response, data, options['fields'])
        return response

    def _populate_document_fields_from_response(self, response, document, fields):
        """

        @param response:
        @type response: pylastica.response.Response
        @param document:
        @type document: pylastica.document.Document
        @param fields: list of field names to be populated, or '_source' if whole document should be updated
        @type fields: list of str or str
        """
        response_data = response.data
        if fields == '_source':
            if '_source' in response_data['get'] and isinstance(response['get']['_source'], dict):
                document.data = response['get']['_source']
        else:
            keys = fields.split(',')
            data = document.data
            for key in keys:
                if key in response_data['get']['fields']:
                    data[key] = response_data['get']['fields'][key]
                elif key in data:
                    del data[key]
            document.data = data

    def delete_documents(self, docs):
        """
        Bulk delete documents
        @param docs:
        @type docs: list of pylastica.document.Document
        @return:
        @rtype: pylastica.bulk.ResponseSet
        """
        assert isinstance(docs, list) and len(docs) > 0, "docs must be a list of at least one document: %r" % docs
        return pylastica.bulk.Bulk(self).add_documents(docs, pylastica.bulk.Action.OP_TYPE_DELETE).send()

    #TODO: finish, starting with getStatus()
